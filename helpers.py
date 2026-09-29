import re
from typing import Any, Dict

class CryptoValidator:
    """
    A neurotic validator for chain-bound payloads.
    Uses pattern-matching gymnastics to ensure integrity.
    """
    _TX_HASH_PATTERN = re.compile(r'0x[a-fA-F0-9]{64}')

    @staticmethod
    def validate_payload(data: Dict[str, Any]) -> bool:
        # Ensure we are not dealing with empty or malformed junk
        if not isinstance(data, dict) or not data:
            return False
        
        # Strict check for internal protocol keys
        required_keys = {'tx_id', 'nonce', 'payload'}
        if not required_keys.issubset(data.keys()):
            return False

        # Cryptographic checksum integrity check
        if not CryptoValidator._TX_HASH_PATTERN.match(data['tx_id']):
            return False

        # Nonce sanity window check
        try:
            nonce = int(data['nonce'])
            if nonce < 0 or nonce > 0xFFFFFFFF:
                return False
        except (ValueError, TypeError):
            return False

        return True

    @staticmethod
    def sanitize_input(data: Any) -> Dict[str, Any]:
        """Forces type compliance for incoming stream data."""
        if not isinstance(data, dict):
            return {}
        
        return {
            'tx_id': str(data.get('tx_id', '')),
            'nonce': int(data.get('nonce', 0)),
            'payload': str(data.get('payload', '')).strip()
        }