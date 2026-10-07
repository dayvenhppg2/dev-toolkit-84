from typing import List, Dict, Union, Optional
from decimal import Decimal

class CryptoProcessor:
    """Orchestrates normalization of raw exchange price feeds."""

    def __init__(self, precision: int = 8) -> None:
        self.precision: int = precision

    def normalize_stream(self, raw_data: List[Dict[str, Union[str, float]]]) -> List[Dict[str, Decimal]]:
        """Converts unstructured raw trades into high-precision decimal dictionaries."""
        processed: List[Dict[str, Decimal]] = []
        for entry in raw_data:
            try:
                clean_entry: Dict[str, Decimal] = {
                    "price": Decimal(str(entry["p"])).quantize(Decimal(f"1.{'0' * self.precision}")),
                    "volume": Decimal(str(entry["q"]))
                }
                processed.append(clean_entry)
            except (KeyError, ValueError, TypeError):
                continue
        return processed

    def get_vwap(self, data: List[Dict[str, Decimal]]) -> Optional[Decimal]:
        """Calculates volume weighted average price using lazy accumulation."""
        if not data:
            return None
            
        total_val: Decimal = sum((d['price'] * d['volume'] for d in data), Decimal('0'))
        total_vol: Decimal = sum((d['volume'] for d in data), Decimal('0'))
        
        return total_val / total_vol if total_vol > 0 else Decimal('0')