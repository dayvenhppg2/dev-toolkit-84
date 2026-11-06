import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'config.json', defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}
        self.settings = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def __getitem__(self, key: str) -> Any:
        return self.settings.get(key)

    def __getattr__(self, name: str) -> Any:
        if name in self.settings:
            return self.settings[name]
        raise AttributeError(f'Config key {name} not found')

    def __repr__(self) -> str:
        return f'<ConfigLoader sources={list(self.settings.keys())}>'