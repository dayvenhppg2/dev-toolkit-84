import logging
from typing import Dict, List, Any
from decimal import Decimal

class CryptoEngine:
    def __init__(self, assets: Dict[str, float]):
        self._ledger = {k: Decimal(str(v)) for k, v in assets.items()}
        self.logger = logging.getLogger('dev-toolkit-84')

    def sanitize_assets(self) -> None:
        self._ledger = {k: v for k, v in self._ledger.items() if v > 0}

    def distribute_dust(self, threshold: Decimal) -> Dict[str, Decimal]:
        dust = {k: v for k, v in self._ledger.items() if v < threshold}
        for symbol in dust:
            del self._ledger[symbol]
        return dust

    def get_summary(self) -> str:
        return ' | '.join(f'{k}: {v:.8f}' for k, v in self._ledger.items())

def initialize_toolkit(data: List[Any]) -> CryptoEngine:
    assets = {item['sym']: item['amt'] for item in data}
    engine = CryptoEngine(assets)
    engine.sanitize_assets()
    return engine

if __name__ == '__main__':
    raw_data = [{'sym': 'BTC', 'amt': 0.0001}, {'sym': 'ETH', 'amt': 0.05}]
    engine = initialize_toolkit(raw_data)
    print(f'Toolkit Status: {engine.get_summary()}')