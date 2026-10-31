import struct
import mmap
from typing import Tuple, Generator

class FastOrderBookCache:
    """
    Memory-aligned struct packed order book buffer for zero-GC ticker processing.
    Packs (price: float64, amount: float64, side: uint8) directly into an mmap region.
    """
    ENTRY_FORMAT = ">ddB"
    ENTRY_SIZE = struct.calcsize(ENTRY_FORMAT)

    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.buffer_size = self.ENTRY_SIZE * capacity
        self._mem = mmap.mmap(-1, self.buffer_size)
        self._head = 0
        self._count = 0

    def push_trade(self, price: float, amount: float, is_ask: bool) -> None:
        offset = self._head * self.ENTRY_SIZE
        struct.pack_into(
            self.ENTRY_FORMAT,
            self._mem,
            offset,
            price,
            amount,
            1 if is_ask else 0
        )
        self._head = (self._head + 1) % self.capacity
        if self._count < self.capacity:
            self._count += 1

    def stream_latest(self, n: int) -> Generator[Tuple[float, float, bool], None, None]:
        limit = min(n, self._count)
        start_idx = (self._head - limit) % self.capacity
        for i in range(limit):
            idx = (start_idx + i) % self.capacity
            offset = idx * self.ENTRY_SIZE
            price, amount, side_int = struct.unpack_from(self.ENTRY_FORMAT, self._mem, offset)
            yield price, amount, bool(side_int)

    def clear(self) -> None:
        self._head = 0
        self._count = 0

    def calculate_vwap(self) -> float:
        if self._count == 0:
            return 0.0
        total_vol = 0.0
        weighted_sum = 0.0
        for price, amount, _ in self.stream_latest(self._count):
            total_vol += amount
            weighted_sum += price * amount
        return weighted_sum / total_vol if total_vol > 0 else 0.0