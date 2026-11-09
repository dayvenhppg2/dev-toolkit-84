import logging
from typing import Any, Callable, TypeVar, Optional

T = TypeVar('T')

class CryptoCircuitBreaker:
    def __init__(self, retries: int = 3):
        self.retries = retries

    def __call__(self, func: Callable[..., T]) -> Callable[..., Optional[T]]:
        def wrapper(*args: Any, **kwargs: Any) -> Optional[T]:
            attempt = 0
            while attempt < self.retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempt += 1
                    logging.warning(f'Attempt {attempt} failed: {e}')
                except Exception as e:
                    logging.critical(f'Fatal crypto error: {e}')
                    return None
            return None
        return wrapper

@CryptoCircuitBreaker(retries=3)
def fetch_order_book(symbol: str) -> dict:
    # Simulate volatile exchange behavior
    import random
    if random.random() < 0.3:
        raise ConnectionError('Exchange node offline')
    return {'symbol': symbol, 'bid': 50000.0, 'ask': 50001.0}

def process_trade(symbol: str):
    data = fetch_order_book(symbol)
    if data is None:
        logging.error(f'Trade processing aborted for {symbol}')
        return
    print(f'Order placed for {symbol}: {data}')

if __name__ == '__main__':
    process_trade('BTC-USD')