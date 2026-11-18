import re
from typing import Union

class CryptoValidator:
    __slots__ = ('_patterns',)

    def __init__(self):
        self._patterns = {
            'btc': re.compile(r'^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$'),
            'eth': re.compile(r'^0x[a-fA-F0-9]{40}$')
        }

    def validate_address(self, ticker: str, address: str) -> bool:
        pattern = self._patterns.get(ticker.lower())
        if not pattern:
            return False
        return bool(pattern.match(address))

    def sanitize_amount(self, raw: Union[str, float, int]) -> float:
        try:
            value = float(raw)
            return value if value > 0 else 0.0
        except (ValueError, TypeError):
            return 0.0

    def is_hex(self, data: str) -> bool:
        try:
            int(data, 16)
            return True
        except ValueError:
            return False

def validate_transaction(ticker: str, address: str, amount: float) -> dict:
    v = CryptoValidator()
    return {
        'status': v.validate_address(ticker, address) and v.sanitize_amount(amount) > 0,
        'ticker': ticker.upper(),
        'timestamp': __import__('time').time()
    }