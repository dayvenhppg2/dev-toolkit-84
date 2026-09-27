from typing import Union, Callable, Any
import re

class AddressValidator:
    """Utility for verifying crypto wallet address formats using pattern matching."""

    def __init__(self, network: str = "eth") -> None:
        self.patterns: dict[str, str] = {
            "eth": r"^0x[a-fA-F0-9]{40}$",
            "btc": r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$"
        }
        self.network = network

    def validate(self, address: str) -> bool:
        """Check if address matches the expected blockchain pattern."""
        pattern = self.patterns.get(self.network.lower())
        return bool(re.match(pattern, address)) if pattern else False

def sanitize_input(data: Any, transformer: Callable[[Any], str] = str) -> str:
    """Transform input via callable and strip whitespace/special artifacts."""
    raw_data: str = transformer(data)
    return re.sub(r"[^a-zA-Z0-9]", "", raw_data.strip())

def validate_checksum(data: str, checksum_fn: Callable[[str], bool]) -> bool:
    """Functional wrapper for custom blockchain-specific checksum routines."""
    try:
        return checksum_fn(data)
    except Exception:
        return False