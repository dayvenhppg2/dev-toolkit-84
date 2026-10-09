import hashlib
import time
from typing import Dict, Any, Optional

class ChainedLogger:
    """
    A cryptographic chained logger that links each log entry to the previous one
    using SHA-256 hashes, creating a tamper-evident audit trail for crypto operations.
    """
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        self.last_hash: str = "0" * 64

    def _calculate_hash(self, timestamp: float, level: str, message: str, prev_hash: str) -> str:
        """Calculates the SHA-256 hash of the log record combined with the previous hash."""
        payload = f"{timestamp}-{level}-{self.node_id}-{message}-{prev_hash}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def log(self, level: str, message: str, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Logs a message, seals it with a cryptographic hash, and advances the chain.
        
        Returns the constructed log block dictionary.
        """
        timestamp = time.time()
        current_hash = self._calculate_hash(timestamp, level, message, self.last_hash)
        
        log_entry: Dict[str, Any] = {
            "timestamp": timestamp,
            "level": level.upper(),
            "node_id": self.node_id,
            "message": message,
            "extra": extra or {},
            "prev_hash": self.last_hash,
            "hash": current_hash
        }
        
        print(f"[{log_entry['level']}] | Hash: {current_hash[:16]}... | {message}")
        self.last_hash = current_hash
        return log_entry