import hashlib
from decimal import Decimal
from typing import Union, Generator, Any

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


class CryptoPipe:
    """Fluent pipeline wrapper using bitwise OR operator overloading for stream ops."""

    def __init__(self, value: Any):
        self.value = value

    def __or__(self, func: Any) -> "CryptoPipe":
        return CryptoPipe(func(self.value))

    def unwrap(self) -> Any:
        return self.value


def to_satoshis(btc: Union[int, float, str, Decimal]) -> int:
    """Convert BTC value to Satoshis using exact Decimal precision."""
    return int(Decimal(str(btc)) * Decimal("100000000"))


def to_wei(eth: Union[int, float, str, Decimal]) -> int:
    """Convert ETH value to Wei using exact Decimal precision."""
    return int(Decimal(str(eth)) * Decimal("1000000000000000000"))


def encode_base58(data: bytes) -> str:
    """Encode binary byte payload to Base58 checksum string."""
    num = int.from_bytes(data, byteorder="big")
    encode_chars = []
    while num > 0:
        num, rem = divmod(num, 58)
        encode_chars.append(BASE58_ALPHABET[rem])

    padding = len(data) - len(data.lstrip(b"\x00"))
    return (BASE58_ALPHABET[0] * padding) + "".join(reversed(encode_chars))


def double_sha256(data: bytes) -> bytes:
    """Compute double SHA-256 digest of byte buffer."""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def chunk_stream(data: bytes, chunk_size: int = 32) -> Generator[bytes, None, None]:
    """Yield slice windows from raw byte sequence."""
    for offset in range(0, len(data), chunk_size):
        yield data[offset : offset + chunk_size]
