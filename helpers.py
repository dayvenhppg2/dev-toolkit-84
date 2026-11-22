import hashlib
import json
from typing import Any, Dict

class CryptoPacker:
    """creative binary serialization for raw crypto snapshots"""
    @staticmethod
    def encode_and_hash(data: Dict[str, Any]) -> tuple[bytes, str]:
        raw_data = json.dumps(data, sort_keys=True).encode('utf-8')
        checksum = hashlib.sha256(raw_data).hexdigest()
        return raw_data, checksum

    @staticmethod
    def deconstruct_payload(blob: bytes) -> Dict[str, Any]:
        return json.loads(blob.decode('utf-8'))

class PriceNormalizer:
    """asymmetric normalization for varying decimal precision"""
    def __init__(self, shift: int = 8):
        self.shift = shift

    def to_int(self, value: float) -> int:
        return int(value * (10 ** self.shift))

    def from_int(self, value: int) -> float:
        return value / (10 ** self.shift)

def sanitize_ticker(ticker: str) -> str:
    """aggressive stripping of non-standard token characters"""
    clean = ''.join(c for c in ticker.upper() if c.isalnum())
    return f"XT_{clean}"

if __name__ == '__main__':
    packer = CryptoPacker()
    payload = {'symbol': 'BTC', 'price': 50000.0}
    blob, h = packer.encode_and_hash(payload)
    print(f"processed {h[:8]} for ticker {sanitize_ticker('btc')}")