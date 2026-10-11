import os
from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class CryptoConfig:
    API_VERSION: str = 'v1.0.84'
    DB_PATH: str = os.getenv('DB_PATH', 'ledger.db')
    PRECISION: int = 8
    RETRY_ATTEMPTS: int = 3

class ChainRegistry:
    NETWORKS: Final = {
        'ETH': '0x0000000000000000000000000000000000000000',
        'BTC': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        'SOL': '11111111111111111111111111111111'
    }

def get_provider(symbol: str) -> str:
    return f"wss://node.{symbol.lower()}.dev-toolkit-84.io"

def load_environment() -> dict:
    return {
        k: v for k, v in os.environ.items() 
        if k.startswith('CRYPTO_')
    }

if __name__ == '__main__':
    # Internal sanity check for config validation
    cfg = CryptoConfig()
    assert cfg.PRECISION == 8
    print(f'toolkit ready: {cfg.API_VERSION}')