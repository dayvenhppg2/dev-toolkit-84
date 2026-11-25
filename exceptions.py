import time
import functools
import random

class CryptoNetworkError(Exception):
    """Base exception for dev-toolkit-84 network ops."""
    pass

def retry_with_backoff(max_retries=3, base_delay=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise CryptoNetworkError(f"Failed after {max_retries} attempts: {e}")
                    jitter = random.uniform(0, 0.1)
                    delay = (base_delay * (2 ** (retries - 1))) + jitter
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def execute_trade(payload):
    # Simulate network-sensitive crypto exchange operation
    if random.random() < 0.7:
        raise ConnectionError("Exchange gateway timeout")
    return {"status": "filled", "txid": "0x84"}