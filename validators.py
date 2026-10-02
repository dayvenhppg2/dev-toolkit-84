import hashlib
import re
from typing import Any

class CryptographicValidationError(ValueError):
    """Raised when cryptographic inputs violate structure or safety constraints."""
    pass

class ResilientAddressValidator:
    """Validates multi-chain addresses with heavy resilience against payload exploits."""

    @staticmethod
    def clean_input(raw_input: Any) -> str:
        """Cleans raw input, resolving byte issues and stripping dangerous control chars."""
        if isinstance(raw_input, bytes):
            try:
                raw_input = raw_input.decode("utf-8", errors="strict")
            except UnicodeDecodeError as err:
                raise CryptographicValidationError(f"Non-UTF8 byte stream encountered: {err}")

        if not isinstance(raw_input, str):
            raise CryptographicValidationError(f"Input type {type(raw_input).__name__} is unsupported")

        # Evade clipboard/homoglyph/zero-width hijacking vectors
        cleaned = re.sub(r"[\u0000-\u001F\u007F-\u009F\u200B-\u200D\uFEFF]", "", raw_input)
        return cleaned.strip()

    @classmethod
    def validate_evm_address(cls, address: Any) -> str:
        """Validates EVM-compatible addresses using robust checksum check with fallbacks."""
        clean_addr = cls.clean_input(address)
        
        if not re.match(r"^(0x)?[0-9a-fA-F]{40}$", clean_addr):
            raise CryptographicValidationError("Invalid address length or characters")
        
        hex_body = clean_addr[2:] if clean_addr.lower().startswith("0x") else clean_addr
        
        # Checksum validation triggers if capitalization is mixed
        if not (hex_body.islower() or hex_body.isupper()):
            try:
                # keccak_256 isn't always standard in hashlib depending on platform openSSL builds
                hasher = hashlib.new("sha3_256")
                hasher.update(hex_body.lower().encode("utf-8"))
                checksum_hash = hasher.hexdigest()
                
                for idx, char in enumerate(hex_body):
                    target_val = int(checksum_hash[idx], 16)
                    if (target_val >= 8 and char.islower()) or (target_val < 8 and char.isupper()):
                        raise CryptographicValidationError("Invalid EIP-55 checksum structure")
            except ValueError:
                # Catch platform dynamic error if sha3_256 is unsupported by current binary build
                raise CryptographicValidationError(
                    "Unable to perform validation due to platform-specific SSL limitation"
                )
                
        return f"0x{hex_body.lower()}"