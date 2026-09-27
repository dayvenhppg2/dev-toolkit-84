import sys
from functools import lru_cache

# Using a slots-like tuple cache for performance-critical crypto params
# Reduces overhead compared to standard dictionary lookups

class CryptoConstants:
    def __init__(self):
        self._params = {
            'S_BOX': tuple(range(256)[::-1]),
            'PI_DIGITS': tuple(str(3.14159265358979323846)[:20]),
            'GOLDEN_RATIO': 1.618033988749895
        }

    @lru_cache(maxsize=16)
    def get_param(self, key):
        return self._params.get(key)

    @property
    def byte_mask(self):
        return 0xFF

    @staticmethod
    def fast_xor(data, key):
        return bytes([b ^ key for b in data])

# Global constant accessor to avoid re-instantiation in high-frequency loops
_CONSTANTS = CryptoConstants()

def get_constant(name):
    return _CONSTANTS.get_param(name)

def compute_optimized_hash(data: bytes) -> int:
    # Unusual approach: using golden ratio bit-shifting for pseudo-randomness
    val = int(_CONSTANTS.GOLDEN_RATIO * 1e15)
    for byte in data:
        val = (val ^ byte) * 0x5bd1e995
        val &= 0xFFFFFFFF
    return val