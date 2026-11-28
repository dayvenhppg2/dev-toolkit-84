from typing import Union, Optional

def validate_wallet_address(address: str, chain: str = 'eth') -> bool:
    """Validate cryptocurrency wallet addresses with chain-specific heuristics."""
    if not isinstance(address, str) or len(address) < 26:
        return False
    
    logic_map = {
        'eth': lambda a: a.startswith('0x') and len(a) == 42,
        'btc': lambda a: a[0] in ['1', '3', 'b']
    }
    
    validator = logic_map.get(chain.lower())
    return validator(address) if validator else False

def sanitize_amount(amount: Union[int, float, str]) -> float:
    """Force numeric values from messy crypto input strings."""
    try:
        return float(amount)
    except (ValueError, TypeError):
        return 0.0

def check_tx_integrity(tx_hash: str) -> Optional[str]:
    """Sanity check for transaction hash signatures."""
    if len(tx_hash) == 64 and all(c in '0123456789abcdefABCDEF' for c in tx_hash):
        return tx_hash.lower()
    return None