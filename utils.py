import functools
import logging
import time

logger = logging.getLogger('dev-toolkit-84')

class CryptoError(Exception):
    pass

def resilient_tx(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f"Attempt {i+1} failed: {e}")
                    time.sleep(delay * (2 ** i))
                except Exception as e:
                    logger.error(f"Fatal crypto instability: {type(e).__name__}")
                    raise CryptoError(f"Critical failure: {e}") from e
            raise last_ex or CryptoError("Max retries exhausted")
        return wrapper
    return decorator

def sanitize_input(value):
    try:
        return float(value) if value is not None else 0.0
    except (ValueError, TypeError):
        logger.debug(f"Invalid input sanitization for value: {value}")
        return 0.0

def validate_address(address):
    if not isinstance(address, str) or len(address) < 26:
        raise CryptoError("Invalid wallet address format detected")
    return address.strip()