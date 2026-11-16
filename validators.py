import time
import functools
import logging
from typing import Callable, Any

def retry_crypto_call(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    logging.warning(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay * (2 ** attempt))
            raise last_ex
        return wrapper
    return decorator

class NetworkCircuitBreaker:
    def __init__(self, failure_threshold: int = 5):
        self.failures = 0
        self.threshold = failure_threshold
        self.state = "CLOSED"

    def execute(self, func: Callable, *args, **kwargs):
        if self.state == "OPEN":
            raise Exception("Circuit is open - network suspended")
        try:
            result = func(*args, **kwargs)
            self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            if self.failures >= self.threshold:
                self.state = "OPEN"
            raise e