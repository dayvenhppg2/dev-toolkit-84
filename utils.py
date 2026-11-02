import time
import functools
import random
from typing import Callable, Any

def jitter_backoff(retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempt = 0
            current_delay = delay
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    sleep_time = current_delay * (1 + random.random())
                    time.sleep(sleep_time)
                    current_delay *= backoff
        return wrapper
    return decorator

@jitter_backoff(retries=5, delay=0.5)
def secure_request(url: str):
    import urllib.request
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.status