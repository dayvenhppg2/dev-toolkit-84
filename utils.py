import time
import functools
import random
from typing import Callable, Any

def exponential_backoff(max_retries: int = 3, base_delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        raise e
                    # Adding jitter for blockchain network congestion avoidance
                    jitter = random.uniform(0, 0.1 * base_delay)
                    delay = (base_delay * (2 ** (retries - 1))) + jitter
                    time.sleep(delay)
        return wrapper
    return decorator

@exponential_backoff(max_retries=5)
def fetch_price_data(ticker: str):
    # Simulate network instability for crypto API endpoints
    if random.random() < 0.7:
        raise ConnectionError(f"node sync latency for {ticker}")
    return {"symbol": ticker, "price": 42069.0}