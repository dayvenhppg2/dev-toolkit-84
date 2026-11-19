import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, file_path: str, defaults: Dict[str, Any] = None):
        self.path = file_path
        self.defaults = defaults or {}
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

def get_crypto_config():
    defaults = {
        "rpc_url": "https://mainnet.infura.io/v3/",
        "timeout": 30,
        "retry_attempts": 3
    }
    return ConfigLoader("settings.json", defaults)