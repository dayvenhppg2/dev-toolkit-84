import logging
from typing import Any, Callable, TypeVar, ParamSpec

T = TypeVar('T')
P = ParamSpec('P')

class CryptoCircuitBreaker:
    def __init__(self, limit: int = 3):
        self.failures = 0
        self.limit = limit

    def __call__(self, func: Callable[P, T]) -> Callable[P, T | None]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | None:
            if self.failures >= self.limit:
                logging.critical('circuit open: aborting execution')
                return None
            try:
                result = func(*args, **kwargs)
                self.failures = max(0, self.failures - 1)
                return result
            except (ConnectionError, TimeoutError) as e:
                self.failures += 1
                logging.error(f'transient error caught: {e}')
                return None
            except Exception as e:
                logging.exception(f'fatal protocol error: {e}')
                raise
        return wrapper

def sanitize_payload(data: Any) -> dict:
    if not isinstance(data, dict):
        return {'status': 'err', 'raw': str(data)}
    return {k: str(v).strip() for k, v in data.items() if v is not None}

@CryptoCircuitBreaker(limit=2)
def execute_trade(pair: str, amount: float) -> str:
    if amount <= 0:
        raise ValueError('negative liquidity detected')
    return f'executing {pair} @ {amount}'