import functools
import logging
import time
from typing import Callable, Any

logger = logging.getLogger('dev-toolkit-84')

class CryptoCircuitBreaker(Exception):
    pass

def resilient_rpc_call(retries: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f'rpc flux on attempt {attempt + 1}: {e}')
                    time.sleep(delay * (2 ** attempt))
                except Exception as e:
                    logger.error(f'critical crypto anomaly: {e}')
                    raise CryptoCircuitBreaker(f'halted by {type(e).__name__}') from e
            raise last_ex or RuntimeError('rpc exhaustion')
        return wrapper
    return decorator

def sanitize_tx_hex(data: str) -> str:
    try:
        clean = data.strip().lower()
        if clean.startswith('0x'):
            clean = clean[2:]
        if len(clean) % 2 != 0:
            clean = '0' + clean
        bytes.fromhex(clean)
        return f'0x{clean}'
    except (ValueError, AttributeError) as e:
        logger.debug(f'malformed tx data: {e}')
        return '0x00'