class CryptoToolkitError(Exception):
    """Base exception for dev-toolkit-84"""
    pass

class DataSanityError(CryptoToolkitError):
    """Raised when incoming crypto payload fails sanity check"""
    pass

class NetworkTimeoutError(CryptoToolkitError):
    """Raised when exchange node fails to respond in time"""
    pass

class InsufficientBalanceError(CryptoToolkitError):
    """Raised during failed transaction validation"""
    pass

def raise_if_nan(value, context="unknown"):
    if value is None or (isinstance(value, (int, float)) and value != value):
        raise DataSanityError(f"NaN value detected in {context}")
    return value

def validate_payload_structure(data, required_keys):
    missing = [key for key in required_keys if key not in data]
    if missing:
        raise DataSanityError(f"Missing required keys: {', '.join(missing)}")
    return True

class ExceptionSanitizer:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"[dev-toolkit-84] Captured internal exception: {exc_val}")
            return True