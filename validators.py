import hashlib
import re
from typing import Dict, Any, Callable, Tuple

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def base58_decode(v: str) -> bytes:
    decimal = 0
    for char in v:
        decimal = decimal * 58 + BASE58_ALPHABET.index(char)
    res = decimal.to_bytes((decimal.bit_length() + 7) // 8, byteorder="big")
    pad = len(v) - len(v.lstrip("1"))
    return b"\x00" * pad + res

def validate_btc_legacy(address: str) -> bool:
    try:
        if not (26 <= len(address) <= 35):
            return False
        decoded = base58_decode(address)
        if len(decoded) != 25:
            return False
        payload, checksum = decoded[:-4], decoded[-4:]
        expected = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        return checksum == expected
