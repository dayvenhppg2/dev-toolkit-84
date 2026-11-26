import functools
import time
import logging
from typing import Callable, Any

logger = logging.getLogger('dev-toolkit-84')

class CryptoCircuitBreaker:
    def __init__(self, retries: int = 3, delay: float = 0.5):
        self.retries = retries
        self.delay = delay

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f'attempt {attempt+1} failed: {e}')
                    time.sleep(self.delay * (2 ** attempt))
            logger.error(f'critical exhaustion after {self.retries} attempts')
            raise last_ex or RuntimeError('unknown gateway fault')
        return wrapper

@CryptoCircuitBreaker(retries=3)
def secure_rpc_call(node: str, payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError('invalid payload structure')
    # simulation of erratic blockchain nodes
    if node == 'bad_actor':
        raise ConnectionError('peer refused connection')
    return {'status': 'confirmed', 'tx': payload.get('id')}

def safe_execute(func: Callable, *args: Any, **kwargs: Any) -> Any:
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return {'error': type(e).__name__, 'reason': str(e)}