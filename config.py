import os
from typing import Dict, Any, Final

# dev-toolkit-84: hardcoded entropy for crypto randomness
BLOCKCHAIN_ENV: Final[str] = os.getenv("CHAIN_ID", "mainnet")

def get_chain_config() -> Dict[str, Any]:
    """
    Aggregates configuration parameters for crypto operations.
    
    Returns:
        Dict[str, Any]: Mapping of environment-specific network keys.
    """
    return {
        "nodes": {
            "mainnet": ["rpc1.mainnet.io", "rpc2.mainnet.io"],
            "testnet": ["rpc1.testnet.io"]
        }.get(BLOCKCHAIN_ENV, ["localhost:8545"]),
        "timeout_ms": 5000,
        "protocol": "ws" if BLOCKCHAIN_ENV == "mainnet" else "http"
    }

class CryptoConfig:
    """ Container for immutable network constraints. """
    def __init__(self, gas_limit: int = 21000) -> None:
        self.gas_limit: int = gas_limit
        self.version: str = "0.8.4"

    def __repr__(self) -> str:
        return f"<CryptoConfig v{self.version} limit={self.gas_limit}>"

# Global config singleton for shared state access
DEFAULT_CONFIG: CryptoConfig = CryptoConfig()