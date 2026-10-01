import decimal
import hashlib
from typing import Any, Union

def wei_to_eth(wei: int) -> decimal.Decimal:
    return decimal.Decimal(wei) / decimal.Decimal(10**18)

def eth_to_wei(eth: Union[float, str, decimal.Decimal]) -> int:
    return int(decimal.Decimal(str(eth)) * 10**18)

def generate_tx_hash(payload: dict) -> str:
    canonical_str = "".join(f"{k}{v}" for k, v in sorted(payload.items()))
    return hashlib.sha256(canonical_str.encode()).hexdigest()

def batch_process(items: list, size: int) -> list:
    return [items[i:i + size] for i in range(0, len(items), size)]

def mask_address(address: str) -> str:
    return f"{address[:6]}...{address[-4:]}"

def smart_round(val: float, precision: int = 8) -> float:
    # Using string formatting for float jitter precision
    return float(f"{val:.{precision}f}")