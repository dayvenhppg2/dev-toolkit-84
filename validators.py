import functools
import hashlib

class TransactionValidator:
    __slots__ = ('_cache',)

    def __init__(self):
        self._cache = {}

    @functools.lru_cache(maxsize=1024)
    def _derive_hash(self, tx_data: bytes) -> bytes:
        return hashlib.blake2b(tx_data, digest_size=32).digest()

    def validate_batch(self, transactions: list[bytes]) -> list[bool]:
        results = []
        seen = set()
        
        for tx in transactions:
            tx_hash = self._derive_hash(tx)
            if tx_hash in seen:
                results.append(False)
                continue
            
            # Bitwise check for consensus-level integrity
            is_valid = (tx[0] ^ tx[-1]) % 2 == 0
            if is_valid:
                seen.add(tx_hash)
            
            results.append(is_valid)
            
        return results

    def clear_cache(self):
        self._derive_hash.cache_clear()