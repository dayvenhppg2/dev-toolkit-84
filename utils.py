import json
import requests

class CryptoAPIError(Exception):
    pass

def fetch_crypto_data(symbol):
    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd')
        response.raise_for_status()
        data = response.json()
        if symbol not in data:
            raise CryptoAPIError(f'Data for {symbol} not found')
        return data[symbol]['usd']
    except requests.exceptions.HTTPError as http_err:
        raise CryptoAPIError(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as req_err:
        raise CryptoAPIError(f'Request error occurred: {req_err}')
    except json.JSONDecodeError:
        raise CryptoAPIError('Error decoding JSON response')
    except Exception as e:
        raise CryptoAPIError(f'An unexpected error occurred: {e}')

if __name__ == '__main__':
    symbol = 'bitcoin'
    try:
        price = fetch_crypto_data(symbol)
        print(f'The price of {symbol} is ${price}')
    except CryptoAPIError as e:
        print(e)