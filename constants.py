BASE_API_URL = 'https://api.crypto.com'

DEFAULT_TIMEOUT = 30  # in seconds

SUPPORTED_COINS = {
    'BTC': {'symbol': '₿', 'full_name': 'Bitcoin'},
    'ETH': {'symbol': 'Ξ', 'full_name': 'Ethereum'},
    'LTC': {'symbol': 'Ł', 'full_name': 'Litecoin'},
    'XRP': {'symbol': '✕', 'full_name': 'Ripple'},
}

ERROR_CODES = {
    400: 'Bad Request',
    401: 'Unauthorized',
    404: 'Not Found',
    500: 'Internal Server Error',
}

CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'JPY': '¥',
    'GBP': '£',
}

class CryptoConstants:
    @staticmethod
    def get_supported_coins():
        return SUPPORTED_COINS.keys()
    
    @staticmethod
    def get_error_message(code):
        return ERROR_CODES.get(code, 'Unknown Error')

    @staticmethod
    def get_currency_symbol(currency):
        return CURRENCY_SYMBOLS.get(currency, '')