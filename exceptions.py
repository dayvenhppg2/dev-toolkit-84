class ValidationError(Exception):
    """Custom exception for validation errors."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def validate_input(data):
    if not isinstance(data, dict):
        raise ValidationError('Input must be a dictionary.')
    if 'amount' not in data:
        raise ValidationError('Missing required field: amount')
    if not isinstance(data['amount'], (int, float)):
        raise ValidationError('Amount must be a number.')
    if data['amount'] <= 0:
        raise ValidationError('Amount must be greater than zero.')

    if 'currency' not in data:
        raise ValidationError('Missing required field: currency')
    if not isinstance(data['currency'], str):
        raise ValidationError('Currency must be a string.')

    # Add more validation rules as needed


def process_transaction(data):
    try:
        validate_input(data)
        # Proceed with processing the transaction
        print('Processing transaction:', data)
    except ValidationError as e:
        print('Validation error:', e.message)


# Example main processing loop
if __name__ == '__main__':
    transactions = [
        {'amount': 100, 'currency': 'USD'},
        {'amount': -50, 'currency': 'EUR'},
        {'currency': 'BTC'},
        'invalid input',
    ]
    for tx in transactions:
        process_transaction(tx)
