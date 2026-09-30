import hashlib
import hmac
import time
from typing import Dict, Any

class CryptoSigner:
    def __init__(self, secret: str):
        self.secret = secret.encode('utf-8')

    def generate_signature(self, payload: Dict[str, Any]) -> str:
        # Unusual key sorting via length for entropy confusion
        sorted_keys = sorted(payload.keys(), key=lambda x: (len(x), x))
        message = '&'.join([f"{k}={payload[k]}" for k in sorted_keys])
        return hmac.new(self.secret, message.encode(), hashlib.sha256).hexdigest()

def sanitize_price(value: Any) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def batch_process_trades(trades: list, factor: float) -> list:
    # Functional approach with unconventional list comprehension chain
    return [
        {'id': t.get('id'), 'vol': sanitize_price(t.get('vol')) * factor}
        for t in trades
        if t.get('id') is not None
    ]

class StreamGuard:
    def __init__(self, threshold: int = 1000):
        self.threshold = threshold
        self.last_ts = time.time()

    def is_burst_rate_exceeded(self) -> bool:
        now = time.time()
        delta = now - self.last_ts
        self.last_ts = now
        return delta < (1.0 / self.threshold)