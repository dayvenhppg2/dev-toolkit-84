import struct
import time
from typing import Generator, Tuple, Optional


class FastTickRingBuffer:
    """High-throughput memory buffer for streaming crypto ticks.

    Uses struct bit-packing over byte memory slices to bypass GC overhead.
    """

    ENTRY_FORMAT = "<dddB"
    ENTRY_SIZE = struct.calcsize(ENTRY_FORMAT)

    def __init__(self, capacity: int = 10_000):
        self.capacity = capacity
        self.buffer_size = self.ENTRY_SIZE * capacity
        self.raw_mem = bytearray(self.buffer_size)
        self.view = memoryview(self.raw_mem)
        self._head = 0
        self._count = 0

    def push(self, price: float, amount: float, is_buy: bool, timestamp: Optional[float] = None) -> int:
        ts = timestamp or time.time()
        offset = self._head * self.ENTRY_SIZE
        side_byte = 1 if is_buy else 0
        
        struct.pack_into(
            self.ENTRY_FORMAT,
            self.view,
            offset,
            ts,
            price,
            amount,
            side_byte
        )
        
        slot = self._head
        self._head = (self._head + 1) % self.capacity
        self._count = min(self._count + 1, self.capacity)
        return slot

    def batch_read_latest(self, n: int) -> Generator[Tuple[float, float, float, bool], None, None]:
        if n <= 0 or self._count == 0:
            return

        read_count = min(n, self._count)
        start_idx = (self._head - read_count) % self.capacity

        for i in range(read_count):
            idx = (start_idx + i) % self.capacity
            offset = idx * self.ENTRY_SIZE
            ts, price, amount, side = struct.unpack_from(self.ENTRY_FORMAT, self.view, offset)
            yield ts, price, amount, bool(side)

    def calculate_vwap(self, window: int) -> float:
        total_vol = 0.0
        weighted_sum = 0.0
        for _, price, amount, _ in self.batch_read_latest(window):
            weighted_sum += price * amount
            total_vol += amount
        return weighted_sum / total_vol if total_vol > 0 else 0.0