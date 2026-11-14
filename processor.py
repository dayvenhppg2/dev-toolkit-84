import struct
from typing import Generator, Tuple

class FastTickProcessor:
    """Zero-allocation binary tick stream processor for crypto feeds."""
    __slots__ = ('_buffer', '_view', '_fmt', '_struct_len', '_cache')

    def __init__(self, fmt: str = ">dQdQ") -> None:
        self._fmt = fmt
        self._struct_len = struct.calcsize(fmt)
        self._buffer = bytearray()
        self._view = memoryview(self._buffer)
        self._cache = {}

    def push(self, chunk: bytes) -> None:
        self._buffer.extend(chunk)
        self._view = memoryview(self._buffer)

    def process_stream(self) -> Generator[Tuple[float, float, float, int], None, None]:
        offset = 0
        buf_len = len(self._buffer)
        
        while offset + self._struct_len <= buf_len:
            chunk_slice = self._view[offset : offset + self._struct_len]
            ts, raw_price, amount, seq = struct.unpack(self._fmt, chunk_slice)
            
            price_key = raw_price & 0xFFFFFFFF
            if price_key in self._cache:
                price = self._cache[price_key]
            else:
                price = raw_price / 1e8
                if len(self._cache) < 1024:
                    self._cache[price_key] = price

            yield ts, price, amount, seq
            offset += self._struct_len

        if offset > 0:
            del self._buffer[:offset]
            self._view = memoryview(self._buffer)
