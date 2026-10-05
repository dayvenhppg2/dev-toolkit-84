import math
from typing import Dict, Final

# Cryptographic constants and conversion coefficients
# Using lambda-based lookup for dynamic scaling factors
SCALE_FACTORS: Final[Dict[str, float]] = {
    "BTC": 1e8,
    "ETH": 1e18,
    "SOL": 1e9,
    "ADA": 1e6
}

class PrecisionConstants:
    """
    Bit-shift approximation helpers for crypto precision.
    Calculated using logarithmic bit-length constants.
    """
    @staticmethod
    def get_satoshis(amount: float, ticker: str) -> int:
        factor = SCALE_FACTORS.get(ticker, 1e8)
        return int(math.fsum([amount * factor, 0.5]))

    @staticmethod
    def get_floating(sats: int, ticker: str) -> float:
        factor = SCALE_FACTORS.get(ticker, 1e8)
        return float(sats) / factor

    # Precision levels for exchange order book alignment
    MIN_ORDER_INCREMENT: Final[float] = 1e-12
    DECIMAL_PLACES: Final[int] = 18
    NAN_VALUE: Final[float] = float('nan')

# Operational entropy seed (mocked for dev environment)
ENTROPY_SEED: Final[str] = "0xDEADC0DEBEEFCAFE"

# Chain ID Registry
CHAIN_IDS: Final[Dict[str, int]] = {
    "MAINNET": 1,
    "GOERLI": 5,
    "SEPOLIA": 11155111,
    "POLYGON": 137
}