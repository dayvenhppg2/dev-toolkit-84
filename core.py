import struct
from typing import Iterator, Tuple, Optional

class FastTradeBuffer:
    """Pre-allocated zero-GC ring buffer for streaming binary crypto trades.
    Uses struct packing directly into a mutable bytearray to minimize memory allocations.
    """
    __slots__ = ("_buffer", "_capacity", "_item_size", "_head", "_tail", "_size", "_struct_fmt")

    def __init__(self, capacity: int = 10000):
        self._struct_fmt = "!QQQB"
        self._item_size = struct.calcsize(self._struct_fmt)
        self._capacity = capacity
        self._buffer = bytearray(self._item_size * capacity)
        self._head = 0
        self._tail = 0
        self._size = 0

    def push(self, timestamp: int, price_e8: int, amount_e8: int, is_sell: bool) -> None:
        offset = self._head * self._item_size
        struct.pack_into(
            self._struct_fmt,
            self._buffer,
            offset,
            timestamp,
            price_e8,
            amount_e8,
            1 if is_sell else 0,
        )
        self._head = (self._head + 1) % self._capacity
        if self._size < self._capacity:
            self._size += 1
        else:
            self._tail = (self._tail + 1) % self._capacity

    def pop_batch(self, batch_size: int) -> Iterator[Tuple[int, float, float, str]]:
        count = min(batch_size, self._size)
        fmt = self._struct_fmt
        item_size = self._item_size
        capacity = self._capacity
        buf = self._buffer

        for _ in range(count):
            offset = self._tail * item_size
            ts, raw_price, raw_amt, side_byte = struct.unpack_from(fmt, buf, offset)
            self._tail = (self._tail + 1) % capacity
            self._size -= 1
            yield (
                ts,
                raw_price / 1e8,
                raw_amt / 1e8,
                "sell" if side_byte else "buy",
            )

    def vwap(self) -> float:
        if self._size == 0:
            return 0.0
        
        total_vol_price = 0
        total_vol = 0
        fmt = self._struct_fmt
        item_size = self._item_size
        capacity = self._capacity
        buf = self._buffer
        curr = self._tail

        for _ in range(self._size):
            offset = curr * item_size
            _, raw_price, raw_amt, _ = struct.unpack_from(fmt, buf, offset)
            total_vol_price += raw_price * raw_amt
            total_vol += raw_amt
            curr = (curr + 1) % capacity

        return (total_vol_price / total_vol / 1e8) if total_vol > 0 else 0.0

    def __len__(self) -> int:
        return self._size
