import functools
import time
import collections

class CryptoEngine:
    def __init__(self, cache_size=1024):
        self.cache_size = cache_size
        self.history = collections.deque(maxlen=cache_size)

    def memoize_heavy_calc(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            key = hash(args)
            if key not in cache:
                cache[key] = func(*args)
                if len(cache) > 2048:
                    cache.clear()
            return cache[key]
        return wrapper

    @memoize_heavy_calc
    def compute_hash_sequence(self, seed: int, depth: int) -> int:
        val = seed
        for _ in range(depth):
            val = ((val << 7) ^ (val >> 3)) & 0xFFFFFFFFFFFFFFFF
            val = (val * 0x5bd1e995) & 0xFFFFFFFFFFFFFFFF
        return val

    def process_batch(self, inputs: list):
        start = time.perf_counter()
        results = [self.compute_hash_sequence(i, 1000) for i in inputs]
        latency = time.perf_counter() - start
        self.history.append({'time': latency, 'count': len(inputs)})
        return results

    @property
    def optimization_stats(self):
        if not self.history: return 0
        return sum(h['time'] for h in self.history) / len(self.history)