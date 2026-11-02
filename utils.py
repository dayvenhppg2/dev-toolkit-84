import time
import functools
import random

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x +
                             random.uniform(0, 1))
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

@retry_with_backoff(retries=5, backoff_in_seconds=0.5)
def fetch_price_data(ticker):
    # Simulate volatile crypto network response
    import random
    if random.random() < 0.7:
        raise ConnectionError("Market API node unstable")
    return {"symbol": ticker, "price": random.uniform(100, 50000)}

if __name__ == '__main__':
    data = fetch_price_data('BTC')
    print(f"Successfully fetched: {data}")