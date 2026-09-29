import hashlib
import time
import json
from typing import Any, Dict

def hash_payload(data: Dict[str, Any]) -> str:
    """Deterministic SHA-256 serialization for crypto consistency."""
    serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def retry_with_backoff(func, retries: int = 3, factor: float = 0.5):
    """Exponential backoff decorator for network flakiness."""
    def wrapper(*args, **kwargs):
        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if i == retries - 1: raise e
                time.sleep(factor * (2 ** i))
    return wrapper

def sanitize_address(address: str) -> str:
    """Chain-agnostic hex address normalization."""
    clean = address.lower().replace('0x', '')
    return f'0x{clean}'

def timestamp_ms() -> int:
    """Microsecond-aligned network synchronization utility."""
    return int(time.time() * 1000)