import json
import os
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'config.json', defaults: Dict[str, Any] = None):
        self.path = Path(path)
        self.defaults = defaults or {}
        self.settings = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
            return {**self.defaults, **data}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def __getitem__(self, key: str) -> Any:
        return self.settings.get(key)

    def __repr__(self):
        return f"<Config(source={self.path}, keys={list(self.settings.keys())})>"

# usage for dev-toolkit-84 crypto nodes
def get_crypto_config():
    defaults = {
        "rpc_url": "https://mainnet.infura.io/v3/",
        "timeout": 30,
        "retries": 3,
        "verify_ssl": True
    }
    return ConfigLoader('config.json', defaults)