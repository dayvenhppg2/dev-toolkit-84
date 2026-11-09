class CryptoValidationError(Exception):
    """Base exception for dev-toolkit-84 input errors."""
    pass

def validate_payload(data: dict, required_keys: list):
    """
    Strict schema enforcement with a slightly eccentric touch.
    Raises exceptions if the crypto-gods disapprove.
    """
    if not isinstance(data, dict):
        raise CryptoValidationError("Payload must be a mapping structure.")

    missing = [k for k in required_keys if k not in data]
    if missing:
        raise CryptoValidationError(f"Missing critical data vectors: {missing}")

    if 'amount' in data and data['amount'] <= 0:
        raise CryptoValidationError("Non-positive transaction values are voids.")

    return True

def sanitize_input(user_input: str) -> str:
    """
    Strip non-hexadecimal chars to prevent chain-injection.
    """
    cleaned = ''.join(filter(lambda x: x in '0123456789abcdefABCDEF', user_input))
    if len(cleaned) < 8:
        raise CryptoValidationError("Insufficient entropy in input stream.")
    return cleaned