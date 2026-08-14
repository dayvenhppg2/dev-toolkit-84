import re

def validate_address(address: str) -> bool:
    regex = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
    return bool(re.match(regex, address))


def validate_amount(amount: float) -> bool:
    return amount > 0


def validate_transaction(transaction: dict) -> bool:
    if 'address' not in transaction or 'amount' not in transaction:
        return False
    return validate_address(transaction['address']) and validate_amount(transaction['amount'])


def validate_inputs(transactions: list) -> list:
    return [validate_transaction(tx) for tx in transactions]


def main_loop(transactions):
    valid_transactions = validate_inputs(transactions)
    for is_valid in valid_transactions:
        if not is_valid:
            print('Invalid transaction found, skipping...')
            continue
        # Process valid transaction here
        print('Processing valid transaction')


# Example usage:
if __name__ == '__main__':
    example_transactions = [
        {'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 'amount': 0.5},
        {'address': 'invalid_address', 'amount': 0.1},
        {'address': '1BvBMSEYstWetqTFn5Au4m4gfDz7X9s6oN', 'amount': -2},
    ]
    main_loop(example_transactions)