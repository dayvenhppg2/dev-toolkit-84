import re
from hashlib import sha256

def validate_address(address: str) -> bool:
    pattern = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
    return bool(re.match(pattern, address))


def checksum(address: str) -> str:
    return sha256(address.encode()).hexdigest()[:8]


def is_valid_transaction(tx: dict) -> bool:
    required_keys = {'from', 'to', 'amount', 'fee', 'nonce'}
    if required_keys.issubset(tx.keys()):
        return validate_address(tx['from']) and validate_address(tx['to'])
    return False


def batch_validate_addresses(addresses: list) -> dict:
    results = {address: validate_address(address) for address in addresses}
    return results


def validate_and_process_transactions(transactions: list) -> list:
    valid_transactions = 
        [tx for tx in transactions if is_valid_transaction(tx)]
    return valid_transactions
