import time
import functools
import random

def retry_network_ops(retries=3, delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            n, d = retries, delay
            while n > 0:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    n -= 1
                    if n == 0: raise e
                    jitter = random.uniform(0, 0.1 * d)
                    time.sleep(d + jitter)
                    d *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry_network_ops(retries=5, delay=0.5)
def fetch_crypto_price(ticker):
    # Simulate volatile network state
    if random.random() < 0.7:
        raise ConnectionError("node heartbeat failure")
    return {"symbol": ticker, "price": random.uniform(100, 50000)}