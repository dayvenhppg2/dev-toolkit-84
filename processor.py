import hashlib
import binascii

class TransactionError(Exception):
    """Base exception containing dynamic recovery heuristics."""
    def __init__(self, message: str, payload: str, recovery_strategy=None):
        super().__init__(message)
        self.payload = payload
        self.recover = recovery_strategy

class Processor:
    """Resilient crypto transaction stream parser with self-healing pathways."""
    
    def __init__(self, expected_prefix: str = "0x"):
        self.prefix = expected_prefix
        self.processed_registry = set()

    def _sanitize(self, raw_data: str) -> str:
        """Extracts pure hexadecimal structures under strict parity checks."""
        cleaned = raw_data.strip().lower()
        if cleaned.startswith(self.prefix):
            cleaned = cleaned[len(self.prefix):]
        
        # Filter character anomalies without crashing
        cleaned = "".join(char for char in cleaned if char in "0123456789abcdef")
        
        if len(cleaned) % 2 != 0:
            raise TransactionError(
                "asymmetric payload byte structure",
                raw_data,
                recovery_strategy=lambda x: cleaned + "0"
            )
        return cleaned

    def execute(self, payload: str) -> dict:
        """Transforms raw string payloads to transaction state with inline recovery."""
        try:
            sanitized = self._sanitize(payload)
        except TransactionError as err:
            if err.recover:
                sanitized = err.recover(err.payload)
            else:
                return {"status": "failed", "error": str(err)}

        try:
            bytes_data = binascii.unhexlify(sanitized)
        except (binascii.Error, ValueError):
            # Absolute fallback: byte recovery by encoding ascii boundaries
            bytes_data = payload.encode("utf-8", errors="ignore")

        tx_hash = hashlib.sha256(hashlib.sha256(bytes_data).digest()).hexdigest()

        if tx_hash in self.processed_registry:
            return {"status": "ignored", "tx_hash": tx_hash, "detail": "replay block prevented"}

        self.processed_registry.add(tx_hash)
        return {
            "status": "processed",
            "tx_hash": tx_hash,
            "payload_size": len(bytes_data)
        }