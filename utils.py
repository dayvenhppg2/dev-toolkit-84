import time
import functools
import random
from typing import Callable, Any

def retry_crypto_request(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    wait_time = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(wait_time)
            raise last_exception
        return wrapper
    return decorator

def execute_with_jitter(operation: Callable, *args, **kwargs):
    for i in range(5):
        try:
            return operation(*args, **kwargs)
        except ConnectionError:
            if i == 4: raise
            time.sleep(0.5 * (i + 1))
    return None