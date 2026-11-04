import logging
from functools import wraps

logger = logging.getLogger('dev-toolkit-84')

class CryptoCircuitBreaker(Exception):
    pass

def sanitize_tx(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None:
                raise ValueError('Null transaction hash detected')
            return result
        except (TypeError, ValueError, ConnectionError) as e:
            logger.error(f'tx_fault: {str(e)}')
            return {'status': 'failed', 'reason': type(e).__name__}
        except Exception:
            return {'status': 'critical_halt', 'reason': 'unrecoverable'}
    return wrapper

@sanitize_tx
def fetch_node_state(node_url):
    if not node_url.startswith('http'):
        raise ValueError('Insecure protocol')
    return {'node': node_url, 'synced': True}

def retry_on_fluctuation(attempts=3):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            last_err = None
            for i in range(attempts):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    last_err = e
            raise CryptoCircuitBreaker(f'node_unstable after {attempts} attempts: {last_err}')
        return wrapper
    return decorator