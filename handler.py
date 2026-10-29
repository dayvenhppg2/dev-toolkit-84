from typing import Callable, Any, TypeVar
from functools import wraps
import math
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")

class CryptoEdgeCaseError(Exception):
    """Base exception for unexpected crypto payload states."""
    pass

class NegativeSlippageAnomaly(CryptoEdgeCaseError):
    pass

class DustThresholdViolation(CryptoEdgeCaseError):
    pass

class CorruptedAddressChecksum(CryptoEdgeCaseError):
    pass

class EdgeCaseGuard:
    """Decorator and sanitizer enforcing safe bounds on volatile DEX data."""

    def __init__(self, dust_limit_sats: int = 546, max_slippage_pct: float = 50.0):
        self.dust_limit_sats = dust_limit_sats
        self.max_slippage_pct = max_slippage_pct

    def sanitize_amount(self, satoshis: int) -> int:
        if satoshis < 0:
            raise DustThresholdViolation(f"Negative amount detected: {satoshis}")
        if 0 < satoshis < self.dust_limit_sats:
            logger.warning(f"Clamping dust amount {satoshis} to zero")
            return 0
        return satoshis

    def sanitize_price(self, price: float, benchmark: float) -> float:
        if math.isnan(price) or math.isinf(price) or price <= 0:
            logger.error(f"Invalid price value: {price}. Falling back to benchmark.")
            return benchmark
        
        dev = abs(price - benchmark) / benchmark * 100
        if dev > self.max_slippage_pct:
            raise NegativeSlippageAnomaly(f"Price deviation {dev:.2f}% exceeds threshold")
        
        return price

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except CryptoEdgeCaseError as e:
                logger.error(f"Handled crypto edge case in {func.__name__}: {e}")
                return None
            except ZeroDivisionError:
                logger.critical("Zero liquidity encountered in swap execution")
                return 0.0
            except ValueError as ve:
                if "base58" in str(ve).lower():
                    raise CorruptedAddressChecksum("Invalid Base58 string format") from ve
                raise ve
        return wrapper  # type: ignore
