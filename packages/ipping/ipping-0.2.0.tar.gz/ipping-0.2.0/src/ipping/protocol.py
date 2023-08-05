import struct
from typing import Tuple

# struct.calcsize('QQ') = 16
HEADER_SIZE = 16


def pack_frame(client_id: int, packet_id: int, payload_size: int) -> bytes:
    return struct.pack(f'QQ{payload_size}s', client_id, packet_id, b'')


def unpack_frame(frame: bytes) -> Tuple[int, int, int]:
    client_id, packet_id = struct.unpack_from('QQ', frame)
    payload_size = len(frame) - HEADER_SIZE
    return client_id, packet_id, payload_size
