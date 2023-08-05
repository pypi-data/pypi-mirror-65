import asyncio
import random
import time
from statistics import mean, stdev
from typing import Optional, Tuple
from weakref import WeakValueDictionary

from .protocol import HEADER_SIZE, pack_frame, unpack_frame

Addr = Tuple[str, int]


class UDPPingClientProtocol(asyncio.DatagramProtocol):

    def __init__(
        self,
        on_connection_made: asyncio.Future,
        on_connection_lost: asyncio.Future,
        on_error_received: asyncio.Future,
    ) -> None:
        self.on_connection_made = on_connection_made
        self.on_connection_lost = on_connection_lost
        self.on_error_received = on_error_received

        self.expected_packets: WeakValueDictionary[
            Tuple[int, int], 'asyncio.Future[Tuple[int, Addr]]'
        ] = WeakValueDictionary()

        self.transport: asyncio.DatagramTransport = None  # type: ignore

    def ping_request(
        self,
        client_id: int,
        packet_id: int,
        payload_size: int,
        response_future: 'asyncio.Future[Tuple[int, Addr]]',
    ) -> None:
        self.expected_packets[(client_id, packet_id)] = response_future
        frame = pack_frame(client_id, packet_id, payload_size)
        self.transport.sendto(frame)

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:  # type: ignore[override] # noqa
        self.transport = transport
        self.on_connection_made.set_result(True)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        self.on_connection_lost.set_result(True)

    def datagram_received(self, data: bytes, addr: Addr) -> None:
        client_id, packet_id, payload_size = unpack_frame(data)
        self.expected_packets[(client_id, packet_id)].set_result((payload_size, addr))

    def error_received(self, exc: Exception) -> None:
        print(f'Request error: {exc}')
        # self.on_error_received.set_exception(exc)


class UDPClient:

    def __init__(
        self,
        remote_host: str,
        remote_port: int,
        payload_size: int,
        loop: asyncio.AbstractEventLoop = None
    ) -> None:
        self.remote_addr = (remote_host, remote_port)
        self.payload_size = payload_size

        self.transport: asyncio.DatagramTransport = None  # type: ignore
        self.protocol: UDPPingClientProtocol = None  # type: ignore

        self.client_id = random.randint(0, 2**64 - 1)
        self.packet_counter = 0

        self.loop = loop

    async def connect(self) -> None:
        loop = self.loop or asyncio.get_event_loop()

        connection_made = loop.create_future()
        connection_lost = loop.create_future()
        error_received = loop.create_future()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UDPPingClientProtocol(
                on_connection_made=connection_made,
                on_connection_lost=connection_lost,
                on_error_received=error_received,
            ),
            remote_addr=self.remote_addr
        )

        self.transport = transport  # type: ignore
        self.protocol = protocol  # type: ignore

        await connection_made

    async def stop(self) -> None:
        self.transport.close()

    async def ping_request(self) -> Tuple[int, int, Addr]:
        loop = self.loop or asyncio.get_event_loop()

        packet_id = self.packet_counter
        self.packet_counter += 1
        response_future = loop.create_future()

        self.protocol.ping_request(
            self.client_id, packet_id, self.payload_size, response_future
        )

        timestamp0 = time.perf_counter()
        res = await response_future
        round_trip = (time.perf_counter() - timestamp0) * 1000

        return (round_trip, *res)  # type: ignore


async def start_udp_client(
    remote_host: str,
    remote_port: int,
    timeout: int = 1,
    count: int = -1,
    payload_size: int = 0,
    wait: float = 1.0,
) -> None:
    udp_client = UDPClient(
        remote_host=remote_host,
        remote_port=remote_port,
        payload_size=payload_size,
    )

    run_infite = count < 0

    print(f'PING {remote_host}:{remote_port}: {payload_size} data bytes')

    await udp_client.connect()

    round_trips = []
    transmitted = 0
    received = 0
    try:
        while run_infite or transmitted < count:
            transmitted += 1
            try:
                round_trip, ret_payload_size, addr = await asyncio.wait_for(udp_client.ping_request(), timeout)
            except asyncio.TimeoutError:
                print('Request timeout')
            else:
                received += 1
                round_trips.append(round_trip)
                print(f'{ret_payload_size + HEADER_SIZE} bytes from {addr[0]}:{addr[1]}: time={round_trip:.3f} ms')
            await asyncio.sleep(wait)
    except asyncio.CancelledError:
        await udp_client.stop()

    print('')
    print(f'--- {remote_host}:{remote_port} ping statistics ---')
    print(f'{transmitted} packets transmitted, {received} packets received, '
          f'{100*(transmitted-received)/transmitted:.1f}% packet loss')
    if len(round_trips) > 0:
        if len(round_trips) == 1:
            stats = (float(round_trips[0]),) * 4
        else:
            stats = (min(round_trips), mean(round_trips), max(round_trips), stdev(round_trips))
        print(f'round-trip min/avg/max/stddev = {stats[0]:.3f}/{stats[1]:.3f}/{stats[2]:.3f}/{stats[3]:.3f} ms')
