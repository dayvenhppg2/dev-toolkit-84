import time
import functools
import random

def retry_with_exponential_backoff(max_retries=3, base_delay=1.0, jitter=True):
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
                        raise e
                    
                    delay = base_delay * (2 ** (retries - 1))
                    if jitter:
                        delay += random.uniform(0, 0.5 * delay)
                    
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry_with_exponential_backoff(max_retries=5)
def fetch_crypto_price(ticker):
    # Simulate network instability for crypto API calls
    if random.random() < 0.7:
        raise ConnectionError(f"node synchronization delay for {ticker}")
    return {"symbol": ticker, "price": 50000.0}