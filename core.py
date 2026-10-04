import struct
from typing import Iterator, Tuple


class TradeStreamBuffer:
    """Zero-copy circular ring buffer for microsecond crypto trade tick processing."""

    __slots__ = ('_buffer', '_size_mask', '_head', '_count', '_price_fmt')

    def __init__(self, capacity_pow2: int = 12):
        if capacity_pow2 < 2 or capacity_pow2 > 20:
            raise ValueError("Capacity exponent must be between 2 and 20")
        capacity = 1 << capacity_pow2
        self._size_mask = capacity - 1
        # Layout: double price (8b), double volume (8b), uint64 timestamp_ns (8b) = 24b
        self._buffer = bytearray(capacity * 24)
        self._head = 0
        self._count = 0
        self._price_fmt = struct.Struct('<ddQ')

    def push(self, price: float, volume: float, timestamp_ns: int) -> None:
        idx = (self._head & self._size_mask) * 24
        self._price_fmt.pack_into(self._buffer, idx, price, volume, timestamp_ns)
        self._head += 1
        if self._count <= self._size_mask:
            self._count += 1

    def calculate_vwap(self, lookback_ticks: int) -> float:
        ticks_to_process = min(lookback_ticks, self._count)
        if ticks_to_process == 0:
            return 0.0

        total_volume = 0.0
        weighted_price_sum = 0.0
        buf = memoryview(self._buffer)
        unpack = self._price_fmt.unpack_from

        for i in range(ticks_to_process):
            pos = ((self._head - 1 - i) & self._size_mask) * 24
            price, volume, _ = unpack(buf, pos)
            weighted_price_sum += price * volume
            total_volume += volume

        return weighted_price_sum / total_volume if total_volume > 0 else 0.0

    def stream_ticks(self) -> Iterator[Tuple[float, float, int]]:
        buf = memoryview(self._buffer)
        unpack = self._price_fmt.unpack_from
        start = max(0, self._head - self._count)
        for idx in range(start, self._head):
            pos = (idx & self._size_mask) * 24
            yield unpack(buf, pos)
