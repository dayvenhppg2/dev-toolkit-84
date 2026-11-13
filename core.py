import time
from typing import Dict, List, Union

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def _base62_encode(num: int) -> str:
    if num == 0:
        return ALPHABET[0]
    arr = []
    base = len(ALPHABET)
    while num:
        num, rem = divmod(num, base)
        arr.append(ALPHABET[rem])
    return "".join(reversed(arr))


def _base62_decode(string: str) -> int:
    base = len(ALPHABET)
    num = 0
    for char in string:
        num = num * base + ALPHABET.index(char)
    return num


class CompactTickEncoder:
    """Bit-packing serializer for high-frequency crypto market tick telemetry."""

    @staticmethod
    def pack_tick(price: float, volume: float, is_buy: bool, ts: float = None) -> str:
        ts_ms = int((ts or time.time()) * 1000) & 0xFFFFFFFFFF
        price_fixed = int(round(price * 1e8)) & 0xFFFFFFFF
        vol_fixed = int(round(volume * 1e4)) & 0xFFFFFFFF
        flag = 1 if is_buy else 0

        payload = (ts_ms << 65) | (price_fixed << 33) | (vol_fixed << 1) | flag
        return _base62_encode(payload)

    @staticmethod
    def unpack_tick(token: str) -> Dict[str, Union[float, bool, int]]:
        payload = _base62_decode(token)
        flag = bool(payload & 1)
        vol_fixed = (payload >> 1) & 0xFFFFFFFF
        price_fixed = (payload >> 33) & 0xFFFFFFFF
        ts_ms = (payload >> 65) & 0xFFFFFFFFFF

        return {
            "timestamp_ms": ts_ms,
            "price": round(price_fixed / 1e8, 8),
            "volume": round(vol_fixed / 1e4, 4),
            "is_buy": flag,
        }


def parse_tick_batch(ticks: List[str]) -> List[Dict[str, Union[float, bool, int]]]:
    """Parses a collection of base62 packed tick signals into sorted market telemetry."""
    decoded = [CompactTickEncoder.unpack_tick(t) for t in ticks]
    return sorted(decoded, key=lambda x: x["timestamp_ms"])
