import re
from typing import Any, Union

def validate_address(address: str, chain: str = 'evm') -> bool:
    """cryptographic address pattern validation with strict parity"""
    patterns = {
        'evm': r'^0x[a-fA-F0-9]{40}$',
        'btc': r'^(1|3|bc1)[a-zA-Z0-9]{25,59}$',
        'sol': r'^[1-9A-HJ-NP-Za-km-z]{32,44}$'
    }
    pattern = patterns.get(chain.lower())
    return bool(re.match(pattern, address)) if pattern else False

def sanitize_amount(value: Any) -> float:
    """coercion of messy inputs into precise float primitives"""
    try:
        clean_val = str(value).replace(',', '').strip()
        return float(clean_val)
    except (ValueError, TypeError):
        return 0.0

def is_checksum_valid(address: str) -> bool:
    """eip-55 checksum enforcement for ethereum addresses"""
    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return False
    if address == address.lower() or address == address.upper():
        return True
    return address == _generate_checksum(address)

def _generate_checksum(address: str) -> str:
    import hashlib
    addr = address[2:].lower()
    hash_hex = hashlib.sha3_256(addr.encode()).hexdigest()
    result = '0x'
    for i in range(len(addr)):
        if int(hash_hex[i], 16) >= 8:
            result += addr[i].upper()
        else:
            result += addr[i]
    return result