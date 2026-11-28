import functools
from typing import Any, Callable

class CryptoValidationError(Exception):
    """Custom base exception for dev-toolkit-84 pipeline"""
    pass

def validate_payload(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            data = args[0] if args else kwargs.get('data')
            if not isinstance(data, (dict, list)):
                raise CryptoValidationError("Invalid payload format: expected dict or list")
            if not data:
                raise CryptoValidationError("Empty payload encountered")
            return func(*args, **kwargs)
        except (KeyError, TypeError, AttributeError) as e:
            raise CryptoValidationError(f"Malformed data structure: {str(e)}")
    return wrapper

@validate_payload
def verify_tx_hash(data: dict) -> bool:
    tx_hash = data.get("tx_hash")
    if not isinstance(tx_hash, str) or len(tx_hash) != 64:
        raise CryptoValidationError("Invalid hexadecimal transaction hash")
    return True

def robust_parse(data: Any) -> dict:
    try:
        return dict(data)
    except (ValueError, TypeError):
        return {"status": "error", "raw": str(data)}