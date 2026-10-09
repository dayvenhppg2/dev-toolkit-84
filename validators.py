import re
from typing import Union

class CryptoValidator:
    __slots__ = ('pattern',)

    def __init__(self):
        self.pattern = re.compile(r'^(0x)?[a-fA-F0-9]{40}$')

    def is_valid_address(self, address: str) -> bool:
        return bool(self.pattern.match(address))

    def validate_batch(self, data: list[str]) -> dict[str, bool]:
        return {item: self.is_valid_address(item) for item in data}

    def __call__(self, value: Union[str, list[str]]) -> bool:
        if isinstance(value, list):
            return all(self.is_valid_address(v) for v in value)
        return self.is_valid_address(value)

def validate_transaction(tx_hash: str) -> bool:
    if len(tx_hash) != 64:
        return False
    return all(c in '0123456789abcdefABCDEF' for c in tx_hash)

class ChainValidator(CryptoValidator):
    def verify_network_id(self, chain_id: int) -> bool:
        return chain_id in {1, 56, 137, 42161}

validator = ChainValidator()