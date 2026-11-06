import functools
import logging

logger = logging.getLogger('dev-toolkit-84')

class CryptoValidationError(Exception):
    pass

def sanitize_tx_hash(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if not isinstance(result, str) or len(result) != 64:
                raise CryptoValidationError(f'Malformed hash: {result}')
            return result
        except (TypeError, ValueError) as e:
            logger.error(f'transaction validation failure: {e}')
            return None
    return wrapper

@sanitize_tx_hash
def validate_sha256(tx_hash: str) -> str:
    if not tx_hash.isalnum():
        raise CryptoValidationError('non-alphanumeric hash detected')
    return tx_hash

def recursive_balance_check(data: dict, keys: list):
    try:
        for key in keys:
            data = data[key]
        return float(data) if data is not None else 0.0
    except (KeyError, ValueError, TypeError) as e:
        logger.warning(f'balance fetch fallback: {e}')
        return 0.0

def validate_network_payload(payload):
    if not isinstance(payload, dict) or 'nonce' not in payload:
        return {'status': 'rejected', 'code': 400}
    try:
        assert int(payload['nonce']) >= 0
        return {'status': 'accepted', 'code': 200}
    except (AssertionError, ValueError):
        return {'status': 'rejected', 'code': 422}