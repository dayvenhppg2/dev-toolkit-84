import os
import json
from typing import Any, Dict, Optional

DEFAULT_CRYPTO_CONFIG: Dict[str, Any] = {
    "ETH_RPC_URL": "https://cloudflare-eth.com",
    "CHAIN_ID": 1,
    "MAX_SLIPPAGE_PCT": 0.5,
    "DEFAULT_GAS_LIMIT": 21000,
    "TX_TIMEOUT_SEC": 120,
    "ENABLE_MEV_PROTECTION": True,
    "MEMPOOL_NODES": ["wss://eth-mainnet.ws.alchemyapi.io/v2/demo"],
}

class ConfigLoader:
    """Dynamic configuration loader with environment overrides and strict fallback."""

    def __init__(self, overrides: Optional[Dict[str, Any]] = None):
        self._user_overrides = overrides or {}

    def __getattr__(self, name: str) -> Any:
        key = name.upper()
        if key not in DEFAULT_CRYPTO_CONFIG and key not in self._user_overrides:
            raise AttributeError(f"Configuration key '{name}' is not registered.")

        val = os.getenv(f"CRYPTO_{key}")
        if val is not None:
            return self._cast_type(DEFAULT_CRYPTO_CONFIG.get(key), val)

        if key in self._user_overrides:
            return self._user_overrides[key]

        return DEFAULT_CRYPTO_CONFIG[key]

    @staticmethod
    def _cast_type(reference_val: Any, raw_val: str) -> Any:
        if reference_val is None:
            return raw_val
        target_type = type(reference_val)
        if target_type is bool:
            return raw_val.lower() in ("true", "1", "yes", "on")
        if target_type is list:
            try:
                return json.loads(raw_val)
            except json.JSONDecodeError:
                return [item.strip() for item in raw_val.split(",")]
        try:
            return target_type(raw_val)
        except ValueError:
            return raw_val

    def export_snapshot(self) -> Dict[str, Any]:
        """Export merged configuration snapshot."""
        return {key.lower(): getattr(self, key) for key in DEFAULT_CRYPTO_CONFIG}


config = ConfigLoader()
