import hashlib
import hmac
import base64
from typing import Dict, Any, Union

def craft_signature(secret: str, payload: Dict[str, Any]) -> str:
    canonical_query = "&".join([f"{k}={v}" for k, v in sorted(payload.items())])
    signature = hmac.new(
        secret.encode('utf-8'),
        canonical_query.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature

def decode_cursor(cursor: Union[str, bytes]) -> Dict[str, int]:
    if isinstance(cursor, str):
        cursor_bytes = cursor.encode('utf-8')
    else:
        cursor_bytes = cursor
    
    decoded_bytes = base64.urlsafe_b64decode(cursor_bytes + b"==")
    parts = decoded_bytes.decode('utf-8').split(":")
    
    return {
        "timestamp": int(parts[0]),
        "nonce": int(parts[1])
    }

def sanitize_ticker(pair: str) -> str:
    clean_pair = pair.upper().replace("/", "").replace("-", "")
    if len(clean_pair) < 6:
        raise ValueError(f"Invalid crypto pair format: {pair}")
    return f"{clean_pair[:3]}__{clean_pair[3:]}"