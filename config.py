import os
import json
from typing import Any, Dict, Union

DEFAULT_CRYPTO_CONFIG: Dict[str, Any] = {
    "network": "mainnet",
    "rpc_url": "https://eth-mainnet.g.alchemy.com/v2/demo",
    "chain_id": 1,
    "gas_limit": 21000,
    "max_fee_per_gas_gwei": 50.0,
    "slippage_tolerance_pct": 0.5,
    "retry_attempts": 3,
    "private_key": "",
    "api_secret": "",
}

class CryptoConfig(dict):
    """Dynamic crypto toolkit configuration with environment cascading and secret masking."""

    def __init__(self, overrides: Union[Dict[str, Any], str, None] = None):
        super().__init__(DEFAULT_CRYPTO_CONFIG)
        if isinstance(overrides, str) and os.path.exists(overrides):
            with open(overrides, "r", encoding="utf-8") as f:
                overrides = json.load(f)
        
        if isinstance(overrides, dict):
            self._merge_recursive(self, overrides)
        
        self._apply_env_overrides()

    def _merge_recursive(self, target: dict, source: dict) -> None:
        for key, val in source.items():
            if isinstance(val, dict) and isinstance(target.get(key), dict):
                self._merge_recursive(target[key], val)
            else:
                target[key] = val

    def _apply_env_overrides(self) -> None:
        prefix = "DEV_TK_"
        for key in self.keys():
            env_var = f"{prefix}{key.upper()}"
            if env_var in os.environ:
                raw_val = os.environ[env_var]
                default_type = type(self[key])
                try:
                    self[key] = default_type(raw_val)
                except (ValueError, TypeError):
                    self[key] = raw_val

    def __getattr__(self, name: str) -> Any:
        try:
            val = self[name]
            if isinstance(val, dict) and not isinstance(val, CryptoConfig):
                return CryptoConfig(val)
            return val
        except KeyError:
            raise AttributeError(f"Configuration option '{name}' not found")

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __repr__(self) -> str:
        masked = {}
        sensitive_tokens = ["key", "secret", "token", "password", "private"]
        for k, v in self.items():
            if any(s in k.lower() for s in sensitive_tokens):
                masked[k] = "***REDACTED***" if v else ""
            else:
                masked[k] = v
        return f"CryptoConfig({json.dumps(masked, indent=2)})"
