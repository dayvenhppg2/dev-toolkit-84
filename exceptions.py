import functools
import re
from typing import Any, Callable, Dict
class CryptoException(Exception):
    def __init__(self, message: str, code: int = 1000):
        self.message = message
        self.code = code
        super().__init__(message)
class InvalidInputError(CryptoException):
    def __init__(self, message: str):
        super().__init__(message, 1001)
class BalanceError(CryptoException):
    def __init__(self, message: str):
        super().__init__(message, 1002)
class CryptoKeyError(CryptoException):
    def __init__(self, message: str):
        super().__init__(message, 1003)
def handle_crypto_errors(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
        try:
            result = func(*args, **kwargs)
            return {"success": True, "data": result}
        except CryptoException as e:
            return {"success": False, "error_code": e.code, "error_message": e.message}
        except ValueError as e:
            return {"success": False, "error_code": 999, "error_message": str(e)}
        except Exception as e:
            return {"success": False, "error_code": 500, "error_message": f"Unexpected error: {str(e)}"}
    return wrapper
@handle_crypto_errors
def validate_address(address: str) -> Dict[str, Any]:
    if not isinstance(address, str):
        raise InvalidInputError("Address must be a string")
    if len(address) == 0:
        raise InvalidInputError("Address cannot be empty")
    if len(address) < 42:
        raise InvalidInputError("Address too short for standard format")
    if not re.match(r"^0x[0-9a-fA-F]{40}$", address):
        raise InvalidInputError("Address must be 0x followed by 40 hex chars")
    return {"address": address.lower()}
@handle_crypto_errors
def validate_balance(balance: float, amount: float, fee: float = 0) -> Dict[str, Any]:
    if balance < 0:
        raise BalanceError("Balance cannot be negative")
    if amount <= 0:
        raise InvalidInputError("Transaction amount must be positive")
    if fee < 0:
        raise InvalidInputError("Fee cannot be negative")
    if balance < (amount + fee):
        raise BalanceError(f"Insufficient balance for {amount} + fee {fee}")
    return {"remaining_balance": balance - amount - fee}
@handle_crypto_errors
def validate_private_key(key: str) -> Dict[str, Any]:
    if not isinstance(key, str):
        raise CryptoKeyError("Private key must be a string")
    if len(key) == 0:
        raise CryptoKeyError("Private key cannot be empty")
    if len(key) != 64:
        raise CryptoKeyError("Private key must be 64 hex characters long")
    if key == "0" * 64:
        raise CryptoKeyError("Private key cannot be all zeros")
    if not all(c.lower() in "0123456789abcdef" for c in key):
        raise CryptoKeyError("Private key contains non-hex characters")
    return {"key_length": 64, "valid": True}
def demonstrate_edge_cases() -> None:
    print(validate_address(""))
    print(validate_address("0x123"))
    print(validate_balance(-1.0, 10.0))
    print(validate_balance(100.0, 150.0))
    print(validate_private_key(""))
    print(validate_private_key("0"*64))
    print(validate_private_key("a"*64))
if __name__ == "__main__":
    demonstrate_edge_cases()