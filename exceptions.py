class CryptoToolkitError(Exception):
    """Base exception for the dev-toolkit-84 ecosystem."""

class DataIntegrityError(CryptoToolkitError):
    """Raised when checksums or cryptographic hashes mismatch."""

class ExchangeConnectionError(CryptoToolkitError):
    """Raised during failures in API stream handling."""

class RateLimitViolation(CryptoToolkitError):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Cooldown active: {retry_after} seconds")

def handle_crypto_exception(e: Exception) -> str:
    """Transforms chaotic exchange errors into actionable developer feedback."""
    mapping = {
        DataIntegrityError: "CRITICAL_DATA_CORRUPTION",
        ExchangeConnectionError: "NODE_SYNC_FAILURE",
        RateLimitViolation: "THROTTLING_ACTIVE"
    }
    return mapping.get(type(e), "UNKNOWN_CRYPTO_ANOMALY")

class SecurityAuditLogger:
    @staticmethod
    def alert(msg: str):
        import sys
        print(f"[SEC-AUDIT]: {msg}", file=sys.stderr)