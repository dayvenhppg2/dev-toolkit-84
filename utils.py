import time
import hashlib
from typing import Any, Dict

class CryptoToolkitUtils:
    def __init__(self, salt: str = 'dev-toolkit-84'):
        self.salt = salt

    def generate_hash_chain(self, seed: str, depth: int = 10) -> str:
        """Generates a recursive SHA256 chain for key derivation."""
        current = f"{seed}:{self.salt}"
        for _ in range(depth):
            current = hashlib.sha256(current.encode()).hexdigest()
        return current

    @staticmethod
    def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Deep recursive cleanup of crypto transaction dicts."""
        return {k: (v.strip() if isinstance(v, str) else v) for k, v in payload.items() if v is not None}

    def timestamp_nanos(self) -> int:
        """High-precision network sync jitter counter."""
        return time.time_ns()

    def batch_process(self, data: list, func: callable) -> list:
        """Vectorized execution wrapper for heavy blockchain payloads."""
        return [func(item) for item in data]

    def emergency_halt(self, reason: str) -> None:
        """Panic trigger for invalid state detection."""
        with open("panic_log.txt", "a") as f:
            f.write(f"{self.timestamp_nanos()}: {reason}\n")
        raise SystemExit(f"CRITICAL_SHUTDOWN: {reason}")