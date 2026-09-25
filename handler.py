import time
import random
import functools
from typing import Callable, Any

def retry_crypto_call(max_retries: int = 3, backoff: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    sleep_time = backoff * (2 ** attempt) + (random.uniform(0, 0.1))
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

@retry_crypto_call(max_retries=5, backoff=1.0)
def fetch_price_data(ticker: str) -> dict:
    import requests
    response = requests.get(f"https://api.crypto-service.io/v1/ticker/{ticker}", timeout=5)
    response.raise_for_status()
    return response.json()

def process_market_order(payload: dict):
    try:
        return fetch_price_data(payload.get('pair', 'BTC-USD'))
    except Exception as err:
        return {"status": "failed", "reason": str(err)}