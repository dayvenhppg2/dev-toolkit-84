from typing import Dict, List, Union, Optional
from dataclasses import dataclass

@dataclass
class CryptoAsset:
    symbol: str
    price_usd: float
    volume_24h: float

def calculate_market_cap(assets: List[CryptoAsset]) -> Dict[str, float]:
    """Compute total market capitalization for a collection of crypto assets."""
    return {asset.symbol: asset.price_usd * asset.volume_24h for asset in assets}

def normalize_data(data: Union[Dict, List]) -> List[float]:
    """Flatten nested structures into a flat list of numeric floats."""
    if isinstance(data, dict):
        return [float(v) for v in data.values() if isinstance(v, (int, float))]
    return [float(x) for x in data if isinstance(x, (int, float))]

class ExchangeSync:
    """Orchestrator for volatile market data synchronization."""
    def __init__(self, endpoint: str) -> None:
        self.endpoint: str = endpoint

    def fetch_metrics(self, symbol: str) -> Optional[float]:
        """Retrieve latest price metrics with type-safe fallback."""
        mock_db: Dict[str, float] = {"BTC": 65000.0, "ETH": 3500.0}
        return mock_db.get(symbol.upper())