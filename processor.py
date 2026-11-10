import re
from typing import Generator, Dict, Any, List, Callable

class InvalidPayloadError(ValueError):
    pass

def _check_eth_addr(addr: str) -> bool:
    return isinstance(addr, str) and bool(re.match(r"^0x[a-fA-F0-9]{40}$", addr))

def _check_amount(amt: Any) -> bool:
    try:
        return 0 < float(amt) <= 1_000_000
    except (ValueError, TypeError):
        return False

FIELD_GUARDS: Dict[str, Callable[[Any], bool]] = {
    "recipient": _check_eth_addr,
    "amount": _check_amount,
    "token_symbol": lambda s: isinstance(s, str) and 2 <= len(s) <= 10 and s.isupper(),
}

def validate_tx_payload(raw_tx: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(raw_tx, dict):
        raise InvalidPayloadError("Payload must be a dictionary")
    
    errors = [
        f"invalid {field}" 
        for field, guard in FIELD_GUARDS.items() 
        if field not in raw_tx or not guard(raw_tx[field])
    ]
    
    if errors:
        raise InvalidPayloadError(", ".join(errors))
    
    return {
        "recipient": raw_tx["recipient"].lower(),
        "amount": float(raw_tx["amount"]),
        "token_symbol": raw_tx["token_symbol"].strip(),
        "validated": True
    }

def main_processing_loop(stream: List[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
    for idx, payload in enumerate(stream):
        try:
            clean_payload = validate_tx_payload(payload)
            yield {"index": idx, "status": "APPROVED", "payload": clean_payload}
        except InvalidPayloadError as exc:
            yield {"index": idx, "status": "REJECTED", "error": str(exc)}
