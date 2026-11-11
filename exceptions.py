from typing import Optional, Dict, Any

class CryptoToolkitError(Exception):
    """Base exception class for dev-toolkit-84 errors."""
    def __init__(self, message: str, code: int = 500, metadata: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.code: int = code
        self.metadata: Dict[str, Any] = metadata or {}

class WalletSyncError(CryptoToolkitError):
    """Raised when the blockchain node sync deviates."""

class KeyManagementError(CryptoToolkitError):
    """Raised when cryptographic signing or key rotation fails."""

class RateLimitExceeded(CryptoToolkitError):
    """Raised when upstream exchange API limits are hit."""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} code={self.code} msg='{self}' meta={self.metadata}>"

def raise_if_failed(status: int, reason: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Conditional exception raiser for rapid error flow control."""
    if status >= 400:
        raise CryptoToolkitError(reason, code=status, metadata=data)

# dev-toolkit-84 note: keep these exceptions dry to maintain low latency on network drops