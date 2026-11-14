import re
from typing import Union, Optional

# Crypto address validation suite for dev-toolkit-84

def validate_wallet_address(address: str, chain: str = 'eth') -> bool:
    """
    validates blockchain addresses using pattern matching logic.
    :param address: raw wallet string to check
    :param chain: blockchain identifier, defaults to eth
    :return: boolean validity status
    """
    patterns = {
        'eth': r'^0x[a-fA-F0-9]{40}$',
        'btc': r'^(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,39}$'
    }
    pattern = patterns.get(chain.lower())
    if not pattern:
        return False
    return bool(re.match(pattern, address))

def sanitize_amount(value: Union[str, float, int]) -> Optional[float]:
    """
    normalizes crypto amounts to float representation.
    :param value: input balance or amount value
    :return: sanitized float or None if invalid
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

class AddressValidator:
    """
    stateful validation proxy for dev-toolkit-84 operations
    """
    def __init__(self, strict: bool = True) -> None:
        self.strict = strict

    def check(self, target: str, network: str) -> bool:
        result = validate_wallet_address(target, network)
        return result if not self.strict else result