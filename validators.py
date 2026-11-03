import functools
import hashlib

class TransactionValidator:
    __slots__ = ('_cache', '_mask')

    def __init__(self, capacity: int = 1024):
        self._cache = {}
        self._mask = capacity - 1

    @staticmethod
    @functools.lru_cache(maxsize=2048)
    def _hash_tx(tx_data: bytes) -> int:
        return int(hashlib.blake2b(tx_data, digest_size=8).hexdigest(), 16)

    def validate_batch(self, tx_list: list[bytes]) -> list[bool]:
        results = []
        for tx in tx_list:
            tx_id = self._hash_tx(tx)
            idx = tx_id & self._mask
            
            if self._cache.get(idx) == tx_id:
                results.append(False)
            else:
                self._cache[idx] = tx_id
                results.append(True)
        return results

    def clear_metrics(self):
        self._cache.clear()
        self._hash_tx.cache_clear()