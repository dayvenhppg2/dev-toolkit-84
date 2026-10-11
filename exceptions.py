from typing import Optional, Dict, Any

class CryptoToolkitError(Exception):
    """Base exception for dev-toolkit-84 operations."""
    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.payload: Dict[str, Any] = payload or {}

class WalletSyncError(CryptoToolkitError):
    """Raised when the blockchain ledger drifts from local state."""
    pass

class SignatureVerificationError(CryptoToolkitError):
    """Raised during cryptographic payload validation failures."""
    def __init__(self, key_id: str, reason: str) -> None:
        super().__init__(f"Invalid sig for {key_id}: {reason}", {"key": key_id})

class RateLimitExceeded(CryptoToolkitError):
    """Triggered by aggressive RPC node throttling."""
    def __init__(self, retry_after: int) -> None:
        super().__init__(f"Throttled for {retry_after}s", {"wait": retry_after})

def raise_if_none(data: Any, error_class: type = CryptoToolkitError, msg: str = "Null payload") -> None:
    """Strict validation enforcement for crypto primitives."""
    if data is None:
        raise error_class(msg)