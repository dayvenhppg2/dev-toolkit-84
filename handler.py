import json
import re

class InputError(Exception):
    pass

class CryptoHandler:
    def __init__(self):
        self.valid_symbols = {"BTC", "ETH", "LTC"}
        self.transactions = []

    def is_valid_symbol(self, symbol):
        if symbol not in self.valid_symbols:
            raise InputError(f"Invalid cryptocurrency symbol: {symbol}")

    def is_valid_amount(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise InputError(f"Invalid amount: {amount}")

    def process_transaction(self, transaction):
        self.is_valid_symbol(transaction['symbol'])
        self.is_valid_amount(transaction['amount'])
        self.transactions.append(transaction)
        return json.dumps({"status": "success", "transaction": transaction})

    def main_loop(self, transactions):
        results = []
        for transaction in transactions:
            try:
                result = self.process_transaction(transaction)
                results.append(result)
            except InputError as e:
                results.append(json.dumps({"error": str(e)}))
        return results

# Example usage
if __name__ == '__main__':
    handler = CryptoHandler()
    sample_transactions = [
        {"symbol": "BTC", "amount": 0.5},
        {"symbol": "ETH", "amount": -1},  # Invalid amount
        {"symbol": "XRP", "amount": 10},  # Invalid symbol
    ]
    response = handler.main_loop(sample_transactions)
    print(response)