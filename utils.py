import functools
import time
import logging

logger = logging.getLogger('dev-toolkit-84')

class CryptoCircuitBreaker:
    def __init__(self, retries=3, delay=1):
        self.retries = retries
        self.delay = delay

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f"Transient failure: {e}. Retrying {attempt+1}/{self.retries}")
                    time.sleep(self.delay * (2 ** attempt))
            logger.error(f"Critical failure after {self.retries} attempts")
            raise last_ex
        return wrapper

@CryptoCircuitBreaker(retries=3, delay=0.5)
def fetch_orderbook(exchange_api, symbol):
    data = exchange_api.get(f"/v1/ticker/{symbol}")
    if not data or 'bids' not in data:
        raise ValueError(f"Malformed orderbook data for {symbol}")
    return data

def sanitize_input(value):
    try:
        return float(value) if value is not None else 0.0
    except (TypeError, ValueError):
        logger.debug(f"Invalid input {value}, defaulting to 0.0")
        return 0.0