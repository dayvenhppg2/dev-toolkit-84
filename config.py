import os
import json
from typing import Any, Dict

DEFAULT_CRYPTO_CONFIG: Dict[str, Any] = {
    "network": "mainnet",
    "rpc_endpoint": "https://eth-mainnet.g.alchemy.com/v2/demo",
    "chain_id": 1,
    "gas_limit_multiplier": 1.15,
    "slippage_tolerance": 0.005,
    "enable_mev_protection": True,
    "max_retries": 3,
}

class CryptoConfig:
    """Dynamic hierarchical configuration loader for crypto trading bots."""
    def __init__(self, filepath: str | None = None):
        self._data = DEFAULT_CRYPTO_CONFIG.copy()
        if filepath and os.path.exists(filepath):
            self._load_file(filepath)
        self._apply_env_overrides()

    def _load_file(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            override = json.load(f)
            self._data.update({k: v for k, v in override.items() if k in self._data})

    def _apply_env_overrides(self) -> None:
        for key, default_val in DEFAULT_CRYPTO_CONFIG.items():
            env_key = f"CRYPTO_{key.upper()}"
            if env_key in os.environ:
                raw_val = os.environ[env_key]
                val_type = type(default_val)
                if val_type is bool:
                    self._data[key] = raw_val.lower() in ("true", "1", "yes")
                else:
                    self._data[key] = val_type(raw_val)

    def __getattr__(self, item: str) -> Any:
        if item in self._data:
            return self._data[item]
        raise AttributeError(f"Configuration key '{item}' does not exist")

    def __repr__(self) -> str:
        return f"<CryptoConfig network={self._data['network']} chain_id={self._data['chain_id']}>"
