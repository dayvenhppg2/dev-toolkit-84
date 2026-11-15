import struct
from typing import Generator, Tuple

class FastTickBuffer:
    """High-performance zero-allocation trade tick processing ring buffer using byte packing."""
    __slots__ = ('_buffer', '_capacity', '_head', '_size', '_struct_fmt')

    def __init__(self, capacity: int = 10000):
        # Format: Q (uint64 ts_ms), q (int64 price scaled 1e8), Q (uint64 vol scaled 1e8)
        self._struct_fmt = struct.Struct('>QqQ')
        self._capacity = capacity
        self._buffer = bytearray(self._struct_fmt.size * capacity)
        self._head = 0
        self._size = 0

    def push(self, timestamp_ms: int, price: float, volume: float) -> None:
        """Pushes tick into preallocated byte storage with fixed-point conversion."""
        scaled_price = int(price * 100_000_000)
        scaled_vol = int(volume * 100_000_000)
        offset = self._head * self._struct_fmt.size
        self._struct_fmt.pack_into(self._buffer, offset, timestamp_ms, scaled_price, scaled_vol)
        self._head = (self._head + 1) % self._capacity
        if self._size < self._capacity:
            self._size += 1

    def stream(self) -> Generator[Tuple[int, float, float], None, None]:
        """Yields unpacked tick data directly from binary memoryview."""
        fmt_size = self._struct_fmt.size
        view = memoryview(self._buffer)
        start_idx = (self._head - self._size) % self._capacity
        
        for i in range(self._size):
            idx = (start_idx + i) % self._capacity
            offset = idx * fmt_size
            ts, p_raw, v_raw = self._struct_fmt.unpack_from(view, offset)
            yield ts, p_raw / 100_000_000, v_raw / 100_000_000

    def calculate_vwap(self) -> float:
        """Fast zero-copy Volume-Weighted Average Price execution."""
        if self._size == 0:
            return 0.0
        
        total_pv = 0
        total_v = 0
        fmt_size = self._struct_fmt.size
        view = memoryview(self._buffer)
        start_idx = (self._head - self._size) % self._capacity

        for i in range(self._size):
            idx = (start_idx + i) % self._capacity
            offset = idx * fmt_size
            _, p_raw, v_raw = self._struct_fmt.unpack_from(view, offset)
            total_pv += p_raw * v_raw
            total_v += v_raw

        return (total_pv / total_v) / 100_000_000 if total_v > 0 else 0.0
