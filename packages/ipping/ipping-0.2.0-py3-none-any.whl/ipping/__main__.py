import argparse
import asyncio

from . import start_udp_client


def main_udp(args: argparse.Namespace) -> None:
    coro = start_udp_client(
        args.host,
        args.port,
        count=args.count,
        payload_size=args.packetsize,
        wait=args.wait,
    )
    loop = asyncio.get_event_loop()
    task = loop.create_task(coro)
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
        loop.run_until_complete(task)


def main() -> None:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    parser_udp_ping = subparsers.add_parser('udp')
    parser_udp_ping.add_argument('host')
    parser_udp_ping.add_argument('port', type=int)
    parser_udp_ping.add_argument(
        '-c',
        '--count',
        type=int,
        default=-1,
        help='Stop after sending (and receiving) COUNT packets.'
        ' If this option is not specified, ping will operate until interrupted.'
    )
    parser_udp_ping.add_argument(
        '-s',
        '--packetsize',
        type=int,
        default=48,
        help='Specify the number of data bytes to be sent.'
        ' The default is 48, which translates into 64 UDP data bytes when combined'
        ' with the 16 bytes of ping header data.'
    )
    parser_udp_ping.add_argument(
        '-i',
        '--wait',
        type=float,
        default=1.0,
        help='Wait WAIT seconds between sending each packet.'
        ' The default is to wait for one second between each packet.'
        ' The wait time may be fractional'
    )
    parser_udp_ping.set_defaults(func=main_udp)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
