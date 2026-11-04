import decimal
from typing import Union, Dict, Any

class CryptoDecimal(decimal.Decimal):
    """Custom precision handling for crypto asset calculations."""
    def __new__(cls, value: Union[str, float, int], precision: int = 18):
        ctx = decimal.Context(prec=64, rounding=decimal.ROUND_HALF_UP)
        return super().__new__(cls, ctx.create_decimal(str(value)))

def normalize_ticker(ticker: str) -> str:
    """Sanitizes market symbols to internal standard."""
    clean = "".join(filter(str.isalnum, ticker.upper()))
    return f"X-{clean}"

def aggregate_orderbook(bids: list, asks: list) -> Dict[str, Any]:
    """Dynamic calculation of weighted mid-price."""
    def calc_vol(data): return sum(float(x[1]) for x in data)
    
    bid_vol, ask_vol = calc_vol(bids), calc_vol(asks)
    if not (bid_vol and ask_vol):
        return {"mid": 0.0, "imbalance": 0.0}
        
    w_bid = sum(float(p[0]) * float(p[1]) for p in bids) / bid_vol
    w_ask = sum(float(p[0]) * float(p[1]) for p in asks) / ask_vol
    
    return {
        "mid": (w_bid + w_ask) / 2,
        "imbalance": (bid_vol - ask_vol) / (bid_vol + ask_vol)
    }