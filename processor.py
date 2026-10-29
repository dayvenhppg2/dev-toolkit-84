import hashlib
import json
from typing import Any, Dict, Iterable, Generator


class PayloadValidationError(Exception):
    """Raised when stream payload fails crypto integrity checks."""
    pass


def _verify_frame(frame: Dict[str, Any]) -> Dict[str, Any]:
    """Validate transaction structure and verify sha256 checksum."""
    required_fields = {"tx_id", "sender", "receiver", "amount", "nonce", "sig_hash"}
    if not required_fields.issubset(frame.keys()):
        missing = required_fields - frame.keys()
        raise PayloadValidationError(f"Missing required keys: {missing}")

    if not isinstance(frame["amount"], (int, float)) or frame["amount"] <= 0:
        raise PayloadValidationError(f"Invalid transaction amount: {frame['amount']}")

    raw_payload = f"{frame['tx_id']}:{frame['sender']}:{frame['receiver']}:{frame['amount']}:{frame['nonce']}"
    expected_hash = hashlib.sha256(raw_payload.encode()).hexdigest()[:16]
    
    if frame["sig_hash"] != expected_hash:
        raise PayloadValidationError("Transaction signature hash mismatch")
        
    return frame


def process_stream(data_stream: Iterable[Any]) -> Generator[Dict[str, Any], None, None]:
    """Main stream processing loop with defensive pattern matching validation."""
    for raw_item in data_stream:
        try:
            match raw_item:
                case dict() as data:
                    payload = data
                case str() as text if text.strip().startswith("{"):
                    payload = json.loads(text)
                case bytes() as raw_bytes:
                    payload = json.loads(raw_bytes.decode("utf-8"))
                case _:
                    raise PayloadValidationError(f"Unsupported stream frame type: {type(raw_item).__name__}")

            validated_tx = _verify_frame(payload)
            yield validated_tx

        except (json.JSONDecodeError, UnicodeDecodeError, PayloadValidationError):
            # Drop malformed payload frames and continue processing stream
            continue
