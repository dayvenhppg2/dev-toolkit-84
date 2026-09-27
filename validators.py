import re
from typing import Any, Dict, Optional

class CryptoValidator:
    ADDRESS_PATTERNS = {
        'BTC': r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',
        'ETH': r'^0x[a-fA-F0-9]{40}$'
    }

    @staticmethod
    def validate_tx(data: Dict[str, Any]) -> bool:
        required = {'asset', 'amount', 'address'}
        if not all(k in data for k in required):
            return False
        
        pattern = CryptoValidator.ADDRESS_PATTERNS.get(data['asset'])
        if not pattern or not re.match(pattern, data['address']):
            return False
            
        try:
            amount = float(data['amount'])
            return amount > 0
        except (ValueError, TypeError):
            return False

class InputGuard:
    def __init__(self, validator_func):
        self.validator = validator_func

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if not self.validator(args[0]):
                raise ValueError(f"Invalid crypto payload: {args[0]}")
            return func(*args, **kwargs)
        return wrapper

def sanitize_input(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if CryptoValidator.validate_tx(payload):
        return {k: str(v).strip() for k, v in payload.items()}
    return None