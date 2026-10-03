import re
from typing import Dict, Any, List, Generator, Callable

class CryptoValidationError(Exception):
    """Raised when payload fails crypto payload sanity checks."""
    pass

def is_valid_address(addr: Any) -> bool:
    return isinstance(addr, str) and bool(re.match(r"^0x[a-fA-F0-9]{40}$", addr))

def is_valid_signature(sig: Any) -> bool:
    return isinstance(sig, str) and bool(re.match(r"^0x[a-fA-F0-9]{130}$", sig))

class TransactionProcessor:
    def __init__(self, target_chain_id: int = 1, max_gas: int = 15_000_000):
        self.target_chain_id = target_chain_id
        self.max_gas = max_gas
        self._rules: List[Callable[[Dict[str, Any]], None]] = [
            self._check_addresses,
            self._check_gas_and_value,
            self._check_signature,
        ]

    def _check_addresses(self, tx: Dict[str, Any]) -> None:
        for field in ("to", "from"):
            if field in tx and not is_valid_address(tx[field]):
                raise CryptoValidationError(f"Invalid address for key '{field}': {tx[field]}")

    def _check_gas_and_value(self, tx: Dict[str, Any]) -> None:
        gas = tx.get("gas", 21000)
        val = tx.get("value", 0)
        chain = tx.get("chain_id", self.target_chain_id)
        
        if not isinstance(gas, int) or not (21000 <= gas <= self.max_gas):
            raise CryptoValidationError(f"Gas limit {gas} outside valid window")
        if not isinstance(val, int) or val < 0:
            raise CryptoValidationError(f"Negative or non-integer value: {val}")
        if chain != self.target_chain_id:
            raise CryptoValidationError(f"Mismatch chain ID {chain}, expected {self.target_chain_id}")

    def _check_signature(self, tx: Dict[str, Any]) -> None:
        sig = tx.get("signature")
        if sig is not None and not is_valid_signature(sig):
            raise CryptoValidationError("Malformed ECDSA hex signature")

    def process_queue(self, incoming: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        processed = []
        for idx, payload in enumerate(incoming):
            try:
                if not isinstance(payload, dict):
                    raise CryptoValidationError("Payload must be a dictionary object")
                
                # Execute dynamic validation rule pipeline
                for rule in self._rules:
                    rule(payload)
                
                processed.append({**payload, "status": "valid", "index": idx})
            except CryptoValidationError as err:
                processed.append({"index": idx, "status": "rejected", "reason": str(err)})
        return processed