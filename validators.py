from typing import Any, Dict

class CryptoValidationError(ValueError):
    pass

def validate_payload(data: Dict[str, Any]) -> bool:
    required = {"txid", "amount", "currency"}
    if not isinstance(data, dict):
        raise CryptoValidationError("Payload must be a dictionary mapping")
    
    missing = required - data.keys()
    if missing:
        raise CryptoValidationError(f"Missing critical crypto fields: {list(missing)}")
    
    amount = data.get("amount")
    if isinstance(amount, (int, float)):
        if amount <= 0:
            raise CryptoValidationError("Transaction amount must be strictly positive")
    elif isinstance(amount, str):
        try:
            if float(amount) <= 0:
                raise CryptoValidationError("Transaction amount string must be strictly positive")
        except ValueError as err:
            raise CryptoValidationError(f"Invalid numeric string for amount: {amount}") from err
    else:
        raise CryptoValidationError("Amount field is of unsupported type")

    currency = data["currency"]
    if not isinstance(currency, str) or len(currency) < 3:
        raise CryptoValidationError("Currency ticker must be at least 3 characters")
    
    return True
