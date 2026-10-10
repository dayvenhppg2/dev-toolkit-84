import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Dynamic crypto configuration loader with cascading defaults."""
    def __init__(self, base_path: str = "config.json"):
        self.base_path = base_path
        self.defaults = {
            "rpc_url": "https://mainnet.infura.io/v3/",
            "timeout": 30,
            "retries": 3,
            "gas_strategy": "aggressive"
        }

    def load(self) -> Dict[str, Any]:
        try:
            with open(self.base_path, "r") as f:
                user_config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            user_config = {}
        
        return {**self.defaults, **user_config, **self._env_override()}

    def _env_override(self) -> Dict[str, Any]:
        keys = ["rpc_url", "timeout", "retries", "gas_strategy"]
        return {k: os.getenv(f"DEV_TOOLKIT_{k.upper()}") for k in keys if os.getenv(f"DEV_TOOLKIT_{k.upper()}")}

config = ConfigLoader().load()