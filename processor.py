import hashlib
import hmac
import time
from typing import Generator, Dict, Any, Callable, List

class SecurityException(Exception):
    pass

class CryptographicPayloadProcessor:
    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key
        self._rules: List[Callable[[Dict[str, Any]], bool]] = [
            self._validate_structure,
            self._validate_timestamp,
            self._validate_cryptographic_integrity
        ]

    def _validate_structure(self, payload: Dict[str, Any]) -> bool:
        required = {"tx_hash", "sender", "amount", "timestamp", "mac"}
        return all(key in payload for key in required)

    def _validate_timestamp(self, payload: Dict[str, Any]) -> bool:
        return abs(time.time() - payload.get("timestamp", 0)) < 60.0

    def _validate_cryptographic_integrity(self, payload: Dict[str, Any]) -> bool:
        msg = f"{payload.get('sender')}:{payload.get('amount')}:{payload.get('timestamp')}".encode()
        expected_mac = hmac.new(self.secret_key, msg, hashlib.sha256).hexdigest()
        return hmac.compare_digest(payload.get("mac", ""), expected_mac)

    def process_stream(self, stream: Generator[Dict[str, Any], None, None]) -> Generator[Dict[str, Any], None, None]:
        for index, frame in enumerate(stream):
            try:
                if not all(rule(frame) for rule in self._rules):
                    raise SecurityException(f"Validation failure at frame {index}")
                yield {**frame, "verified_at": time.time(), "sequence_id": index}
            except SecurityException as err:
                yield {"error": str(err), "corrupted_frame": frame, "sequence_id": index}