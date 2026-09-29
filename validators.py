import re
from typing import Any, Dict, Generator, Iterator

class TransactionValidationError(ValueError):
    """Custom exception raised when transaction parameters fail strict validation."""
    pass

class LoopInputValidator:
    """Unorthodox generator-based pipeline validator for streaming crypto transactions."""

    def __init__(self) -> None:
        self.address_regex = re.compile(r"^0x[a-fA-F0-9]{40}$")

    def is_valid_evm_address(self, address: str) -> bool:
        return isinstance(address, str) and bool(self.address_regex.match(address))

    def is_valid_hex_or_int(self, value: Any) -> bool:
        if isinstance(value, int) and value >= 0:
            return True
        if isinstance(value, str):
            try:
                return int(value, 16) >= 0 if value.startswith("0x") else int(value) >= 0
            except ValueError:
                return False
        return False

    def process_and_validate(self, transactions: Iterator[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        """Validates a stream of crypto transaction inputs, filtering malicious or malformed packets."""
        for idx, tx in enumerate(transactions):
            try:
                if not isinstance(tx, dict):
                    raise TransactionValidationError(f"Transaction index {idx} is malformed")
                
                required_keys = {"from_addr", "to_addr", "value", "nonce"}
                if not required_keys.issubset(tx.keys()):
                    raise TransactionValidationError(f"Tx {idx} missing required fields")

                if not (self.is_valid_evm_address(tx["from_addr"]) and self.is_valid_evm_address(tx["to_addr"])):
                    raise TransactionValidationError(f"Invalid EVM address format in Tx {idx}")

                if not self.is_valid_hex_or_int(tx["value"]) or not self.is_valid_hex_or_int(tx["nonce"]):
                    raise TransactionValidationError(f"Invalid numeric representations in Tx {idx}")

                if str(tx["from_addr"]).lower() == str(tx["to_addr"]).lower():
                    raise TransactionValidationError(f"Self-transaction forbidden in Tx {idx}")

                yield tx
            except TransactionValidationError:
                continue