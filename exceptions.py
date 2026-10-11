class CryptoBaseError(Exception):
    """Base exception for dev-toolkit-84 crypto modules."""
    pass

class RateLimitExceeded(CryptoBaseError):
    """Raised when the exchange API throttles requests."""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Cooldown active: {retry_after}s")

class DataIntegrityError(CryptoBaseError):
    """Raised when price feeds or nonces are corrupted."""
    pass

class WalletConnectivityError(CryptoBaseError):
    """Raised when local node communication fails."""
    def __init__(self, code: int, message: str):
        self.code = code
        super().__init__(f"Node failure [{code}]: {message}")

def handle_crypto_error(err: Exception) -> dict:
    """Maps internal crypto exceptions to standardized responses."""
    mapping = {
        RateLimitExceeded: lambda e: {"status": "throttled", "wait": e.retry_after},
        DataIntegrityError: lambda _: {"status": "corrupt", "action": "retry"},
        WalletConnectivityError: lambda e: {"status": "offline", "code": e.code}
    }
    handler = mapping.get(type(err), lambda _: {"status": "unknown_failure"})
    return handler(err)