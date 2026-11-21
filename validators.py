import time
import functools
from typing import Callable, Any

def exponential_backoff(max_attempts: int = 3, initial_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = initial_delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(delay)
                    delay *= 2
            return None
        return wrapper
    return decorator

@exponential_backoff(max_attempts=5)
def fetch_crypto_price(ticker: str) -> float:
    # simulates network jitter for dev-toolkit-84 operations
    import random
    if random.random() < 0.7:
        raise ConnectionError("node synchronization lag")
    return 42069.0