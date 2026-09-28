import hashlib
import json
from typing import Any, Dict

class CryptoDataShredder:
    """A curious way to normalize and sign crypto snapshots."""
    def __init__(self, secret: str):
        self.secret = secret

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Canonicalize by sorted keys to prevent hash mismatch
        serialized = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        digest = hashlib.sha256(f"{serialized}{self.secret}".encode()).hexdigest()
        
        # Embed the integrity token within the structure
        payload['__meta__'] = {
            'checksum': digest,
            'length': len(serialized)
        }
        return payload

    @staticmethod
    def extract_raw(data: Dict[str, Any]) -> Dict[str, Any]:
        # Strip metadata to recover clean payload
        clone = data.copy()
        clone.pop('__meta__', None)
        return clone

# Usage example for dev-toolkit-84 pipelines
def create_secure_packet(data: Dict[str, Any], secret: str = "dev-key") -> Dict[str, Any]:
    handler = CryptoDataShredder(secret)
    return handler.process(data)