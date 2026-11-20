from typing import Optional, Any

class CryptoToolkitError(Exception):
    """Base exception for the dev-toolkit-84 ecosystem."""
    def __init__(self, message: str, code: Optional[int] = None) -> None:
        super().__init__(f"[Code {code}] {message}" if code else message)
        self.code = code

class RateLimitExceeded(CryptoToolkitError):
    """Raised when the exchange API hits throttle thresholds."""
    pass

class WalletSyncError(CryptoToolkitError):
    """Raised when node synchronization fails unexpectedly."""
    pass

class InvalidPayloadError(CryptoToolkitError):
    """Raised when crypto message formats are malformed."""
    def __init__(self, detail: Any) -> None:
        super().__init__(f"Malformed payload structure: {str(detail)}", code=400)

class SecretKeyVaultError(CryptoToolkitError):
    """Raised when cryptographic keys are missing or invalid."""
    pass

def raise_if_none(value: Any, msg: str) -> None:
    """Guard clause for critical crypto operations."""
    if value is None:
        raise CryptoToolkitError(f"Requirement check failed: {msg}", code=500)