import os
import json
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = 'DK84_'):
        self._data = defaults.copy()
        self._load_from_env(env_prefix)

    def _load_from_env(self, prefix: str) -> None:
        for key in self._data:
            env_key = f"{prefix}{key.upper()}"
            val = os.getenv(env_key)
            if val is not None:
                try:
                    self._data[key] = json.loads(val)
                except json.JSONDecodeError:
                    self._data[key] = val

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Key '{name}' not found in crypto config")

def load_toolkit_config() -> CryptoConfig:
    defaults = {
        "rpc_url": "https://mainnet.infura.io/v3/",
        "timeout": 30,
        "retry_limit": 3,
        "debug_mode": False
    }
    return CryptoConfig(defaults)