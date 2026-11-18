import functools
import zlib
import pickle
from typing import Any, Callable

class DataCompressor:
    """High-speed buffer serialization for crypto-node heartbeat packets."""
    def __init__(self, level: int = 6):
        self.level = level
        self._cache = {}

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> bytes:
            key = (func.__name__, args, tuple(kwargs.items()))
            if key not in self._cache:
                data = func(*args, **kwargs)
                serialized = pickle.dumps(data)
                self._cache[key] = zlib.compress(serialized, level=self.level)
            return self._cache[key]
        return wrapper

@DataCompressor(level=9)
def process_node_metrics(node_id: str, load: float, peers: int) -> dict:
    return {
        "id": node_id,
        "load": load,
        "peer_count": peers,
        "status": "active" if load < 0.8 else "throttled",
        "ts": "2023-10-27T00:00:00Z"
    }

if __name__ == "__main__":
    packet = process_node_metrics("node-alpha", 0.45, 12)
    print(f"Serialized heartbeat: {len(packet)} bytes")