import re
from decimal import Decimal


def is_valid_address(address: str) -> bool:
    pattern = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
    return re.match(pattern, address) is not None


def is_valid_amount(amount: str) -> bool:
    try:
        value = Decimal(amount)
        return value > 0
    except InvalidOperation:
        return False


def is_valid_signature(signature: str) -> bool:
    return len(signature) in {128, 130} and all(c in '0123456789abcdef' for c in signature)


def is_recent_timestamp(timestamp: int) -> bool:
    import time
    return (time.time() - timestamp) < 3600  # within the last hour


def validate_transaction(tx):
    return (is_valid_address(tx.get('from')) and
            is_valid_address(tx.get('to')) and
            is_valid_amount(tx.get('amount')) and
            is_valid_signature(tx.get('signature')) and
            is_recent_timestamp(tx.get('timestamp')))
