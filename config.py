import json
import os
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, path: str = 'config.json'):
        self.path = path
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        defaults = {
            "rpc_url": "https://mainnet.infura.io/v3/",
            "retry_attempts": 3,
            "timeout": 30,
            "sandbox_mode": True
        }
        if not os.path.exists(self.path):
            return defaults
        try:
            with open(self.path, 'r') as f:
                user_cfg = json.load(f)
                return {**defaults, **user_cfg}
        except (json.JSONDecodeError, IOError):
            return defaults

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __repr__(self) -> str:
        return f"CryptoConfig({self._data})"

config = CryptoConfig()