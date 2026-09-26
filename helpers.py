import hashlib
from decimal import Decimal, ROUND_DOWN
from typing import Iterator, Tuple, List

SATS_PER_BTC = Decimal('100000000')


def checksum_cascade(data: bytes, pipeline: str = "sha256>sha256") -> bytes:
    """Executes a chain of hash transformations specified by a pipe string."""
    current = data
    for algo in pipeline.split('>'):
        algo_name = algo.strip().lower()
        if hasattr(hashlib, algo_name):
            hasher = getattr(hashlib, algo_name)()
            hasher.update(current)
            current = hasher.digest()
        else:
            raise ValueError(f"Unsupported hash algorithm: {algo_name}")
    return current


def format_sats(sats: int) -> str:
    """Converts satoshis to formatted BTC string with exact decimal precision."""
    btc_val = (Decimal(sats) / SATS_PER_BTC).quantize(Decimal('0.00000001'), rounding=ROUND_DOWN)
    return f"{btc_val:f} BTC"


def decompose_sats(amount: int, denominations: List[int] = None) -> Iterator[Tuple[int, int]]:
    """Decomposes a satoshi balance into target denomination chunks."""
    if denominations is None:
        denominations = [100000000, 10000000, 1000000, 100000, 10000, 1000, 100, 1]
    
    remaining = amount
    for denom in sorted(denominations, reverse=True):
        if remaining <= 0:
            break
        count, remaining = divmod(remaining, denom)
        if count > 0:
            yield denom, count


def mask_address(address: str, keep_ends: int = 4, mask_char: str = "*") -> str:
    """Masks crypto wallet addresses while preserving chain prefix and suffix identity."""
    if len(address) <= keep_ends * 2:
        return address
    middle_len = len(address) - (keep_ends * 2)
    return f"{address[:keep_ends]}{mask_char * min(middle_len, 6)}{address[-keep_ends:]}"
