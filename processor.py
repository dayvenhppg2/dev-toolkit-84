import math
import re
from typing import Dict, Any, List, Generator

class CryptoEdgeCaseError(Exception):
    """Base exception for unexpected block stream payload anomalies."""

class MalformedHashError(CryptoEdgeCaseError):
    pass

class InvalidAmountError(CryptoEdgeCaseError):
    pass

class TransactionProcessor:
    """Resilient transaction stream processor with self-healing edge case handlers."""

    def __init__(self, strict: bool = False):
        self.strict = strict
        self._hex_pattern = re.compile(r'^0x[a-fA-F0-9]{64}$')

    def sanitize_amount(self, value: Any) -> float:
        """Parse crypto amount handling sci-notation, NaN, infinity, and string junk."""
        if value is None:
            return 0.0
        try:
            val = float(value)
            if math.isnan(val) or math.isinf(val) or val < 0:
                raise InvalidAmountError(f"Out of bounds amount value: {value}")
            return val
        except (ValueError, TypeError) as err:
            raise InvalidAmountError(f"Non-numeric amount received: {value}") from err

    def validate_hash(self, tx_hash: str) -> str:
        """Enforce standard 32-byte hex hash format with auto-prefixing fallback."""
        if not isinstance(tx_hash, str):
            raise MalformedHashError(f"Expected string for hash, got {type(tx_hash)}")
        
        cleaned = tx_hash.strip()
        if not cleaned.startswith('0x'):
            cleaned = '0x' + cleaned
            
        if not self._hex_pattern.match(cleaned):
            raise MalformedHashError(f"Invalid 256-bit hex hash: {tx_hash}")
            
        return cleaned.lower()

    def process_raw_stream(self, raw_txs: List[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        """Process stream of raw transaction dictionaries recovery-mode enabled."""
        for idx, raw in enumerate(raw_txs):
            try:
                if not isinstance(raw, dict):
                    raise CryptoEdgeCaseError(f"Malformed payload at index {idx}: expected dict")
                
                clean_tx = {
                    'hash': self.validate_hash(raw.get('hash', '')),
                    'amount': self.sanitize_amount(raw.get('amount', 0)),
                    'nonce': int(raw.get('nonce', 0)) if str(raw.get('nonce', '')).isdigit() else 0,
                    'gas_price': max(0.0, self.sanitize_amount(raw.get('gas_price', 1.0)))
                }
                yield clean_tx
                
            except CryptoEdgeCaseError as e:
                if self.strict:
                    raise e
                yield {
                    'error': str(e),
                    'raw_index': idx,
                    'status': 'quarantined'
                }
