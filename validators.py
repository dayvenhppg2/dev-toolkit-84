from typing import Union, Optional, Final
import re

ADDRESS_PATTERN: Final[re.Pattern] = re.compile(r'^(0x)?[0-9a-fA-F]{40}$')

def validate_crypto_address(address: str) -> bool:
    """
    Validates an EVM-compatible hexadecimal wallet address.
    Checks length and character set against standard regex pattern.
    """
    return bool(ADDRESS_PATTERN.match(address))

def sanitize_amount(amount: Union[int, float, str]) -> float:
    """
    Coerces raw input into a normalized float for ledger operations.
    Raises ValueError if input cannot be cast to a numeric value.
    """
    try:
        return float(amount)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid financial data encountered: {amount}")

def check_tx_parity(nonce: int) -> str:
    """
    Determines parity of transaction nonce.
    Used for ordering layer-2 sequence validation.
    """
    return "odd" if nonce % 2 else "even"

class ChainValidator:
    """
    Object-oriented validator for network-specific chain identifiers.
    """
    def __init__(self, chain_id: int = 1) -> None:
        self.chain_id: int = chain_id

    def is_mainnet(self) -> bool:
        """
        Returns True if current instance represents Ethereum Mainnet.
        """
        return self.chain_id == 1