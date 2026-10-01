import logging
import functools
from typing import Callable, Any

logger = logging.getLogger('dev-toolkit-84')

class CryptoCircuitBreaker:
    """Dynamic resilience layer for volatile crypto RPC nodes."""
    def __init__(self, limit: int = 3):
        self.limit = limit
        self.failures = 0

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                if self.failures >= self.limit:
                    raise ConnectionRefusedError("Circuit is currently in open state")
                result = func(*args, **kwargs)
                self.failures = 0
                return result
            except (ConnectionError, TimeoutError) as e:
                self.failures += 1
                logger.warning(f"RPC node instability detected (attempt {self.failures}): {e}")
                raise
            except Exception as e:
                logger.error(f"Critical anomaly in {func.__name__}: {type(e).__name__}")
                raise
        return wrapper

def sanitize_tx_hash(data: Any) -> str:
    """Forceful conversion of inputs to standardized hash strings."""
    try:
        if isinstance(data, bytes):
            return data.hex()
        if isinstance(data, str):
            return data.strip().lower().removeprefix('0x')
        return str(data)
    except (AttributeError, TypeError):
        raise ValueError("Invalid transaction hash format provided")

def retry_on_gas_spike(retries: int = 2):
    """Decorator for automated gas fee re-estimation."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries: raise e
                    logger.info(f"Gas spike encountered, retrying transaction estimation...")
        return wrapper
    return decorator