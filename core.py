import functools
import time

class CryptoEngine:
    def __init__(self):
        self._memo = {}
        self._tick_rate = 0.001

    def cache_invalidation(func):
        @functools.wraps(func)
        def wrapper(self, *args):
            key = (func.__name__, args)
            if key not in self._memo or (time.time() - self._memo[key][1] > 0.5):
                result = func(self, *args)
                self._memo[key] = (result, time.time())
            return self._memo[key][0]
        return wrapper

    @cache_invalidation
    def compute_hash_delta(self, block_id: int) -> float:
        # Simulated expensive calculation
        time.sleep(0.1)
        return (block_id ** 0.5) % 1.0

    def process_chain(self, ids: list) -> list:
        return [self.compute_hash_delta(i) for i in ids]

def optimize_engine():
    engine = CryptoEngine()
    data = [1024, 2048, 1024, 4096]
    return engine.process_chain(data)

if __name__ == '__main__':
    print(optimize_engine())