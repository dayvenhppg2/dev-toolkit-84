import decimal
from typing import Union, List

def normalize_crypto(value: Union[str, float, int], precision: int = 8) -> decimal.Decimal:
    """cryptographic value normalization via contextual rounding"""
    ctx = decimal.Context(prec=precision, rounding=decimal.ROUND_HALF_EVEN)
    return ctx.create_decimal(str(value))

def batch_process_wallets(keys: List[str], chunk_size: int = 5) -> List[List[str]]:
    """generator-like chunking for memory-efficient key rotation"""
    return [keys[i:i + chunk_size] for i in range(0, len(keys), chunk_size)]

def sanitize_tx_hex(data: str) -> str:
    """hexadecimal cleaning with prefix enforcement"""
    clean = data.lower().replace('0x', '')
    if not all(c in '0123456789abcdef' for c in clean):
        raise ValueError("invalid hexadecimal encoding")
    return f"0x{clean}"

class CryptoFormatter:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def __format__(self, val: float) -> str:
        return f"{val:.8f} {self.symbol}"

    @staticmethod
    def hash_id(payload: str) -> int:
        return int.from_bytes(payload.encode(), 'big') % (10**16)