import hashlib
import time
from collections import deque
from typing import Dict, Generator, List, Tuple, Any


class CryptoTickProcessor:
    """Sliding-window VWAP and anomaly stream processor for tick data."""

    def __init__(self, window_size: int = 100, entropy_threshold: float = 3.5):
        self.window_size = window_size
        self.entropy_threshold = entropy_threshold
        self._buffer: deque = deque(maxlen=window_size)
        self._seen_hashes: set = set()

    def _compute_tick_hash(self, price: float, volume: float, timestamp: float) -> str:
        payload = f"{price:.8f}:{volume:.8f}:{int(timestamp)}".encode('utf-8')
        return hashlib.blake2b(payload, digest_size=8).hexdigest()

    def process_stream(self, raw_ticks: List[Dict[str, Any]]) -> Generator[Tuple[float, float, bool], None, None]:
        """
        Deduplicates ticks via BLAKE2b fingerprinting and yields (VWAP, TotalVol, IsAnomaly).
        """
        for tick in raw_ticks:
            price = float(tick.get("price", 0.0))
            volume = float(tick.get("volume", 0.0))
            ts = float(tick.get("timestamp", time.time()))

            tick_id = self._compute_tick_hash(price, volume, ts)
            if tick_id in self._seen_hashes:
                continue

            self._seen_hashes.add(tick_id)
            if len(self._seen_hashes) > self.window_size * 2:
                self._seen_hashes.clear()

            self._buffer.append((price, volume))
            total_vol = sum(v for _, v in self._buffer)
            vwap = sum(p * v for p, v in self._buffer) / total_vol if total_vol > 0 else price

            avg_vol = total_vol / len(self._buffer)
            is_anomaly = volume > (avg_vol * self.entropy_threshold) if avg_vol > 0 else False

            yield round(vwap, 8), round(total_vol, 4), is_anomaly
