import decimal
from typing import Dict, List, Any

class CryptoProcessor:
    """A slightly opinionated data normalizer for high-precision ledger entries."""

    def __init__(self, precision: int = 18):
        self.context = decimal.Context(prec=precision, rounding=decimal.ROUND_HALF_EVEN)

    def normalize_stream(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Converts all numerical values into fixed-point decimal objects for parity."""
        return [self._scrub(entry) for entry in raw_data]

    def _scrub(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        processed = {}
        for key, value in entry.items():
            if isinstance(value, (str, float, int)) and self._is_numeric(value):
                processed[key] = self.context.create_decimal(value)
            else:
                processed[key] = value
        return processed

    @staticmethod
    def _is_numeric(val: Any) -> bool:
        try:
            decimal.Decimal(str(val))
            return True
        except (decimal.InvalidOperation, ValueError):
            return False

    @staticmethod
    def format_to_wei(amount: decimal.Decimal, decimals: int = 18) -> int:
        """Force scaling to chain-native integer representation."""
        return int(amount * (10 * decimals))

    @classmethod
    def pipeline_wrap(cls, stream: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        proc = cls()
        return proc.normalize_stream(stream)