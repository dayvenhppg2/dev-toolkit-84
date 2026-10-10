import enum
from typing import Final, Dict, Any

class CryptoErrorCodes(enum.IntEnum):
    SUCCESS = 0
    INSUFFICIENT_LIQUIDITY = 1001
    INVALID_NONCE = 1002
    SLIPPAGE_TOLERANCE_EXCEEDED = 1003
    RPC_TIMEOUT = 1004
    UNSUPPORTED_ASSET = 1005

ERROR_MESSAGES: Final[Dict[int, str]] = {
    CryptoErrorCodes.INSUFFICIENT_LIQUIDITY: "Pool depth insufficient for swap execution",
    CryptoErrorCodes.INVALID_NONCE: "Transaction nonce mismatch in local cache",
    CryptoErrorCodes.SLIPPAGE_TOLERANCE_EXCEEDED: "Price movement outside acceptable threshold",
    CryptoErrorCodes.RPC_TIMEOUT: "Node communication heartbeat interrupted",
    CryptoErrorCodes.UNSUPPORTED_ASSET: "Token contract address not found in registry"
}

RETRY_STRATEGY: Final[Dict[str, Any]] = {
    "max_retries": 3,
    "backoff_factor": 1.5,
    "jitter": True,
    "critical_codes": [CryptoErrorCodes.RPC_TIMEOUT, CryptoErrorCodes.INVALID_NONCE]
}

def get_error_desc(code: int) -> str:
    return ERROR_MESSAGES.get(code, "Unknown protocol failure")