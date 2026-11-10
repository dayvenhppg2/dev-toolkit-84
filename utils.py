import time
import random
from functools import wraps

def retry_crypto_ops(max_retries=3, delay=1.0, backoff=2):
    """ decorator for exponential backoff on network calls """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tries, current_delay = 0, delay
            while tries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    tries += 1
                    if tries == max_retries:
                        raise e
                    sleep_time = current_delay * (backoff ** (tries - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry_crypto_ops(max_retries=5, delay=0.5)
def fetch_node_data(endpoint):
    # simulated unstable network operation
    if random.random() < 0.7:
        raise ConnectionError("node offline")
    return {"status": "synced", "block": 1234567}