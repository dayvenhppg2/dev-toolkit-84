import time
import random
import functools
from typing import Callable, Any

def retry_with_backoff(retries: int = 3, backoff_in_seconds: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x, v = 0, backoff_in_seconds
            while x < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    x += 1
                    if x == retries:
                        raise e
                    sleep_time = (v * (2 ** x)) + (random.randint(0, 1000) / 1000)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

class NetworkProcessor:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @retry_with_backoff(retries=5, backoff_in_seconds=0.5)
    def fetch_market_data(self, pair: str):
        # Simulate unstable crypto exchange connectivity
        if random.random() < 0.7:
            raise ConnectionError(f"Exchange {self.endpoint} heartbeat failure")
        return {"pair": pair, "price": random.uniform(30000, 60000)}