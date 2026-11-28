import hashlib
from functools import reduce
from typing import Generator, Callable, Iterable, Dict, Union

class CryptoProcessor:
    """Creative multi-tool processor for common crypto data transformations."""
    
    def __init__(self, seed: int = 0xDEADBEEF):
        self._seed = seed

    def convert_base_units(self, amounts: Iterable[int], decimals: int = 18) -> Generator[float, None, None]:
        """Convert raw blockchain base units (Wei/Satoshi) using floating point stream generator."""
        divisor = 10 ** decimals
        for amt in amounts:
            yield round(amt / divisor, 8)

    def generate_cascading_hash(self, *items: Union[str, bytes]) -> str:
        """Fold multiple payloads into a single deterministic crypto hash cascade."""
        def _fold(acc: bytes, curr: Union[str, bytes]) -> bytes:
            payload = curr.encode('utf-8') if isinstance(curr, str) else curr
            return hashlib.sha256(acc + payload).digest()
        
        initial = self._seed.to_bytes(4, byteorder='big')
        return reduce(_fold, items, initial).hex()

    @staticmethod
    def apply_rolling_xor(hex_string: str, mask: int = 0x5A) -> str:
        """Obfuscate or unveil hex transactions via position-indexed rolling XOR sequence."""
        clean_hex = hex_string.removeprefix("0x")
        raw = bytes.fromhex(clean_hex)
        transformed = bytes(b ^ ((mask + idx) & 0xFF) for idx, b in enumerate(raw))
        return f"0x{transformed.hex()}"

    def audit_batch_signatures(self, sigs: Iterable[str], validator: Callable[[str], bool]) -> Dict[str, bool]:
        """Process and validate signature arrays using dict comprehension pipelines."""
        return {sig: validator(sig) for sig in sigs if len(sig) > 10}
