import os
import json
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, defaults: Dict[str, Any], path: str = 'config.json'):
        self.path = path
        self.config = defaults.copy()
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    disk_data = json.load(f)
                    self.config.update({k: v for k, v in disk_data.items() if k in self.config})
            except (json.JSONDecodeError, IOError):
                pass

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.config.get(key, fallback)

    def __repr__(self) -> str:
        return f"CryptoConfig({list(self.config.keys())})"

def load_toolkit_config():
    defaults = {
        "rpc_endpoint": "https://mainnet.infura.io/v3/",
        "timeout": 30,
        "retry_limit": 3,
        "cache_enabled": True
    }
    return CryptoConfig(defaults)