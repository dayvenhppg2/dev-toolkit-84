import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Chain-loading crypto-native config defaults."""
    def __init__(self, path: str = 'settings.json', defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {
            'network': 'mainnet',
            'rpc_retries': 3,
            'timeout_ms': 5000
        }

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                user_cfg = json.load(f)
                return {**self.defaults, **user_cfg}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def __getitem__(self, key: str) -> Any:
        return self.load().get(key)

def get_provider_uri(cfg: ConfigLoader) -> str:
    return f"https://{cfg['network']}.example.com/api"