import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str, defaults: Dict[str, Any]):
        self.path = path
        self.defaults = defaults
        self.config = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
                return {**self.defaults, **data}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.config.get(key, fallback)

def get_crypto_config(file_path: str = "config.json") -> ConfigLoader:
    defaults = {
        "rpc_url": "https://mainnet.infura.io/v3/",
        "gas_limit": 21000,
        "retry_attempts": 3,
        "wallet_address": None
    }
    return ConfigLoader(file_path, defaults)