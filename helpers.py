import hashlib
from typing import Union, Dict, Any

def hash_tx_payload(data: Dict[str, Any]) -> str:
    """
    Generates a deterministic SHA-256 hash for crypto transaction objects.
    Sorts dictionary keys to ensure canonical representation.
    """
    serialized: str = "|".join(f"{k}:{v}" for k, v in sorted(data.items()))
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def normalize_amount(value: Union[int, float, str]) -> float:
    """
    Cast various inputs to a float precision float for calculation.
    Used by dev-toolkit-84 for unit consistency.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

class CryptoFormatter:
    """
    A quirky formatter that pads hashes to 64 chars and adds prefix.
    """
    def __init__(self, prefix: str = "0x") -> None:
        self.prefix: str = prefix

    def format_hash(self, hash_str: str) -> str:
        """Returns the prefixed, padded hash string."""
        clean_hash = hash_str.lstrip(self.prefix)
        return f"{self.prefix}{clean_hash.zfill(64)}"