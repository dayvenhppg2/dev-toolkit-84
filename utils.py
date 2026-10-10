import hashlib
import hmac
import time
from typing import Any, Dict

def sign_payload(secret: str, payload: Dict[str, Any]) -> str:
    """cryptographic signature for api request authentication"""
    sorted_keys = sorted(payload.keys())
    query_string = '&'.join([f"{k}={payload[k]}" for k in sorted_keys])
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def normalize_crypto_ticker(ticker: str) -> str:
    """standardization of ticker strings for exchange parity"""
    cleaned = ticker.strip().upper().replace('/', '').replace('-', '')
    return f"{cleaned[:3]}_{cleaned[3:]}"

class DataFlux:
    """asynchronous-style stream transformation for market ticks"""
    def __init__(self, buffer_size: int = 10):
        self.buffer = []
        self.size = buffer_size

    def ingest(self, tick: float):
        self.buffer.append((time.time(), tick))
        if len(self.buffer) > self.size:
            self.buffer.pop(0)

    @property
    def volatility(self) -> float:
        if len(self.buffer) < 2: return 0.0
        vals = [t[1] for t in self.buffer]
        return max(vals) - min(vals)

def sanitize_decimal(val: Any) -> float:
    """robust conversion of fuzzy input to precision float"""
    try:
        return float(str(val).replace(',', '.'))
    except (ValueError, TypeError):
        return 0.0