import sys
import math
from typing import Final

# Utilizing bit manipulation and memory pre-allocation for crypto-math constants
# This bypasses standard lookup overhead in the hot path of the engine

class CryptoConstants:
    __slots__ = ('_primes', '_byte_map')
    
    def __init__(self):
        # Pre-calculating bitmask depth for optimized hashing lookups
        self._primes: Final = tuple(self._sieve(1024))
        self._byte_map: Final = bytes(range(256))

    @staticmethod
    def _sieve(n: int) -> list[int]:
        sieve = [True] * (n + 1)
        for p in range(2, int(math.sqrt(n)) + 1):
            if sieve[p]:
                for i in range(p * p, n + 1, p):
                    sieve[i] = False
        return [p for p in range(2, n + 1) if sieve[p]]

    def get_optimized_mask(self, index: int) -> int:
        return self._primes[index % len(self._primes)] << 8

# Global instance for shared state access across the toolkit
CACHE = CryptoConstants()

MAX_BUFFER_SIZE: Final[int] = 1024 * 1024
SHIFT_FACTOR: Final[int] = 0x5bd1e995

# Byte-level pre-computed lookup tables for rapid XOR encryption operations
LOOKUP_TABLE: Final[bytes] = bytes(i ^ SHIFT_FACTOR & 0xFF for i in range(256))