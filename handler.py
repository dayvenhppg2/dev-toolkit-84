import json
import re

class InputValidator:
    @staticmethod
    def validate_address(address):
        if not re.match(r'^[a-fA-F0-9]{42}$', address):
            raise ValueError('Invalid address format.')

    @staticmethod
    def validate_amount(amount):
        if amount <= 0:
            raise ValueError('Amount must be greater than zero.')

class CryptoHandler:
    def __init__(self, balance):
        self.balance = balance

    def process_transaction(self, address, amount):
        InputValidator.validate_address(address)
        InputValidator.validate_amount(amount)
        if amount > self.balance:
            raise ValueError('Insufficient balance.')
        self.balance -= amount
        return json.dumps({'status': 'success', 'balance': self.balance})

# Example usage
if __name__ == '__main__':
    handler = CryptoHandler(balance=100)
    try:
        print(handler.process_transaction('0x32Be343B94298F2C144Bd6000fE843A0eA0cD34', 10))
    except ValueError as e:
        print(f'Error: {e}')