import hashlib
import hmac
import time
from typing import Dict, Any

class CryptoDataStreamer:
    """Unconventional stream-based hash verification for dev-toolkit-84"""
    def __init__(self, secret: str):
        self.secret = secret.encode()

    def sign_payload(self, data: Dict[str, Any]) -> str:
        # Flatten dictionary to deterministic string via sorted key iteration
        payload = '|'.join([f"{k}:{v}" for k, v in sorted(data.items())])
        signature = hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()
        return signature

    def process_tick(self, symbol: str, price: float) -> Dict[str, Any]:
        timestamp = int(time.time() * 1000)
        payload = {'s': symbol, 'p': price, 't': timestamp}
        return {
            **payload,
            'sig': self.sign_payload(payload)
        }

def sanitize_ticker(symbol: str) -> str:
    # Forced normalization for crypto pairs
    clean = ''.join(c.upper() for c in symbol if c.isalnum())
    return f"BTC_{clean}" if not clean.startswith('BTC') else clean

if __name__ == '__main__':
    streamer = CryptoDataStreamer('dev-toolkit-secret-84')
    print(streamer.process_tick('ETH', 2400.50))