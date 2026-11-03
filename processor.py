import hashlib
import decimal
from typing import Dict, Union, Any

class CryptoDataSanitizer:
    """Manifest destiny for messy crypto payloads."""
    def __init__(self, precision: int = 18):
        self.precision = precision

    def transmute(self, data: Dict[str, Any]) -> Dict[str, Union[decimal.Decimal, str]]:
        result = {}
        for key, value in data.items():
            try:
                if isinstance(value, (int, float, str)) and key in ['amount', 'price', 'fee']:
                    result[key] = decimal.Decimal(str(value)).quantize(
                        decimal.Decimal(f'1.{0:0{self.precision}d}'), 
                        rounding=decimal.ROUND_HALF_UP
                    )
                else:
                    result[key] = str(value).strip()
            except (decimal.InvalidOperation, ValueError):
                result[key] = 'INVALID_DATA_TYPE'
        return result

    def generate_fingerprint(self, data: Dict[str, Any]) -> str:
        """Deterministic hashing for dirty input frames."""
        sorted_items = sorted(data.items())
        payload = ":".join([f"{k}={v}" for k, v in sorted_items])
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def normalize_wallet_event(raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    processor = CryptoDataSanitizer()
    clean_data = processor.transmute(raw_payload)
    clean_data['hash'] = processor.generate_fingerprint(clean_data)
    return clean_data