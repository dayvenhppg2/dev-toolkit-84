import hashlib
import hmac
import time
import json
from typing import Any, Dict

def sign_payload(secret: str, data: Dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

def timestamp_nonce() -> int:
    return int(time.time() * 1000)

def sanitize_currency(pair: str) -> str:
    return pair.replace('-', '').replace('/', '').upper()

class CryptoToolkit:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]

    def format_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'path': f'/v1/{endpoint}',
            'headers': {'X-API-KEY': self.api_key, 'X-NONCE': str(timestamp_nonce())},
            'payload': params
        }

def normalize_amount(value: Any) -> float:
    try:
        return float(f'{float(value):.8f}')
    except (ValueError, TypeError):
        return 0.0

def batch_process(items: list, chunk_size: int = 5):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]