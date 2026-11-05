import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'config.json', defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}
        self.config = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

    def __repr__(self) -> str:
        return f"Config(keys={list(self.config.keys())})"

def get_crypto_config() -> ConfigLoader:
    return ConfigLoader(
        'settings.json',
        defaults={'rpc_url': 'http://localhost:8545', 'timeout': 30, 'retries': 3}
    )