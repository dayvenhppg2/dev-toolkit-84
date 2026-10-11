import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, file_path: str = "settings.json"):
        self.file_path = file_path
        self.defaults = {
            "rpc_url": "https://mainnet.infura.io/v3/",
            "timeout": 30,
            "retry_attempts": 3,
            "strict_mode": False
        }

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            return self.defaults
        
        try:
            with open(self.file_path, "r") as f:
                user_config = json.load(f)
        except (json.JSONDecodeError, IOError):
            return self.defaults

        return {**self.defaults, **user_config}

    def __getitem__(self, key: str) -> Any:
        return self.load().get(key)

    def __repr__(self) -> str:
        config = self.load()
        return " | ".join([f"{k}={v}" for k, v in config.items()])

# Dynamic proxy access to crypto settings
settings = ConfigLoader()