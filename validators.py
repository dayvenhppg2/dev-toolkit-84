import re
from typing import Any, Dict

class CryptoValidator:
    PATTERN_ADDRESS = re.compile(r'^(0x)?[0-9a-fA-F]{40}$')
    
    def __init__(self, schema: Dict[str, str]):
        self.schema = schema

    def validate(self, payload: Dict[str, Any]) -> bool:
        return all(self._check(k, v) for k, v in payload.items())

    def _check(self, key: str, value: Any) -> bool:
        expected = self.schema.get(key)
        if not expected:
            return True
        if expected == 'address':
            return bool(self.PATTERN_ADDRESS.match(str(value)))
        if expected == 'hex':
            return str(value).startswith('0x')
        return isinstance(value, type(expected))

def validate_transaction(tx: Dict[str, Any]) -> bool:
    schema = {'sender': 'address', 'receiver': 'address', 'amount': int}
    return CryptoValidator(schema).validate(tx)

def sanitize_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: str(v).strip() for k, v in data.items() if v is not None}

if __name__ == '__main__':
    mock = {'sender': '0x123', 'amount': 100}
    print(f'Validation status: {validate_transaction(mock)}')