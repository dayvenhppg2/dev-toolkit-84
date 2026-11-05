import time
import functools
import random
import logging

logger = logging.getLogger('dev-toolkit-84')

class NetworkRetryError(Exception):
    """Custom exception for crypto network failures."""
    pass

def exponential_backoff(retries=3, base_delay=1.0, jitter=True):
    """
    A decorator that uses an unusual jittered backoff to 
    thwart rate-limiting nodes in crypto networks.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == retries:
                        logger.error(f"Final attempt failed for {func.__name__}")
                        raise NetworkRetryError(f"Failed after {retries} attempts: {e}")
                    
                    delay = base_delay * (2 ** attempt)
                    if jitter:
                        delay += random.uniform(0, 0.5 * delay)
                    
                    logger.warning(f"Retry {attempt}/{retries} in {delay:.2f}s")
                    time.sleep(delay)
        return wrapper
    return decorator