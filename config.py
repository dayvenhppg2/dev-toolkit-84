import os
import json
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_CRYPTO_SETTINGS: Dict[str, Any] = {
    "network": "mainnet",
    "rpc_endpoint": "https://eth-mainnet.g.alchemy.com/v2/demo",
    "gas_limit_multiplier": 1.15,
    "slippage_tolerance": 0.5,
    "max_retries": 3,
    "enable_mempool_monitoring": False,
    "supported_chains": ["ethereum", "polygon", "arbitrum"]
}

class CryptoConfig:
    """Dynamic configuration loader with crypto defaults and env overrides."""

    def __init__(self, config_path: Union[str, Path, None] = None):
        self._data: Dict[str, Any] = DEFAULT_CRYPTO_SETTINGS.copy()
        if config_path:
            self.load_from_file(config_path)
        self._apply_env_overrides()

    def load_from_file(self, path: Union[str, Path]) -> None:
        file_path = Path(path)
        if file_path.exists() and file_path.suffix == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                user_conf = json.load(f)
                self._data.update(user_conf)

    def _apply_env_overrides(self) -> None:
        prefix = "CRYPTO_TOOLKIT_"
        for key in list(self._data.keys()):
            env_var = prefix + key.upper()
            if env_var in os.environ:
                val = os.environ[env_var]
                orig_type = type(self._data[key])
                if orig_type == bool:
                    self._data[key] = val.lower() in ("true", "1", "yes")
                elif orig_type == list:
                    self._data[key] = [item.strip() for item in val.split(",")]
                else:
                    try:
                        self._data[key] = orig_type(val)
                    except ValueError:
                        self._data[key] = val

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Configuration key '{name}' not found")

    def __getitem__(self, item: str) -> Any:
        return self._data[item]

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __repr__(self) -> str:
        return f"<CryptoConfig network={self._data.get('network')}>"
