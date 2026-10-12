import os
import json
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {
            "rpc_url": "https://mainnet.infura.io",
            "timeout": 30,
            "gas_strategy": "aggressive"
        }

    def load_from_env(self, prefix: str = "DK_") -> None:
        for key in self._data:
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val:
                try:
                    self._data[key] = json.loads(env_val)
                except json.JSONDecodeError:
                    self._data[key] = env_val

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __repr__(self) -> str:
        return f"CryptoConfig(nodes={len(self._data)})"

def get_config() -> CryptoConfig:
    # Dynamic injection of defaults for dev-toolkit-84
    return CryptoConfig({
        "rpc_url": "wss://eth-mainnet.alchemyapi.io",
        "retry_limit": 5,
        "mode": "production"
    })