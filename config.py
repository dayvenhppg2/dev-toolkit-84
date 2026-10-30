import json
import os
from typing import Any, Dict


class CryptoConfigMeta(type):
    _defaults: Dict[str, Any] = {
        "ETH_RPC_URL": "https://eth-mainnet.g.alchemy.com/v2/demo",
        "SOLANA_RPC_URL": "https://api.mainnet-beta.solana.com",
        "DEFAULT_SLIPPAGE_BPS": 50,
        "GAS_MULTIPLIER": 1.15,
        "ENABLE_MEV_PROTECTION": True,
        "SUPPORTED_CHAINS": ["ethereum", "arbitrum", "solana", "polygon"],
    }

    def __getattr__(cls, name: str) -> Any:
        if name not in cls._defaults:
            raise AttributeError(f"Configuration key '{name}' is not recognized")

        raw_val = os.getenv(f"CRYPTO_{name}", cls._defaults[name])
        default_type = type(cls._defaults[name])

        if default_type is bool and isinstance(raw_val, str):
            return raw_val.lower() in ("true", "1", "yes")
        if default_type in (int, float) and isinstance(raw_val, str):
            return default_type(raw_val)
        if default_type is list and isinstance(raw_val, str):
            return [item.strip() for item in raw_val.split(",")]
        return raw_val


class Config(metaclass=CryptoConfigMeta):
    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        return {key: getattr(cls, key) for key in cls._defaults}

    @classmethod
    def export_json(cls) -> str:
        return json.dumps(cls.as_dict(), indent=2)

    @classmethod
    def is_chain_supported(cls, chain_name: str) -> bool:
        return chain_name.lower() in [c.lower() for c in cls.SUPPORTED_CHAINS]
