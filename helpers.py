import functools
import time
import logging
from typing import Callable, Any

logger = logging.getLogger('dev-toolkit-84')

class CryptoCircuitBreaker:
    def __init__(self, retries: int = 3, delay: float = 0.5):
        self.retries = retries
        self.delay = delay

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f"Attempt {attempt+1} failed: {e}")
                    time.sleep(self.delay * (2 ** attempt))
            logger.error("Circuit broken: maximum retries exceeded")
            raise last_ex or RuntimeError("Unknown crypto node failure")
        return wrapper

def safe_decimal_div(numerator: str, denominator: str) -> float:
    try:
        n, d = float(numerator), float(denominator)
        if d == 0:
            return 0.0
        return n / d
    except (ValueError, TypeError):
        return 0.0

def sanitize_tx_hash(tx_hash: Any) -> str:
    if not isinstance(tx_hash, str) or len(tx_hash) < 64:
        return "0x0000000000000000000000000000000000000000000000000000000000000000"
    return tx_hash.lower().strip()