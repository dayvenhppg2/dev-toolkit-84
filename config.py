import os
from dataclasses import dataclass

@dataclass(frozen=True)
class ChainConfig:
    RPC_URL: str = os.getenv('RPC_URL', 'https://mainnet.infura.io/v3/default')
    MAX_RETRIES: int = 5
    TIMEOUT: float = 30.5
    SYMBOL: str = 'ETH'

def get_chain_settings():
    return ChainConfig()

class EnvironmentRegistry:
    def __init__(self):
        self._storage = {
            'DEBUG': os.getenv('APP_DEBUG', 'false').lower() == 'true',
            'TIMEOUT_LIMIT': 60
        }

    def __getitem__(self, key):
        return self._storage.get(key)

    def items(self):
        return self._storage.items()

registry = EnvironmentRegistry()

if __name__ == '__main__':
    # Internal sanity check for config injection
    config = get_chain_settings()
    print(f'Active config for {config.SYMBOL} loaded.')