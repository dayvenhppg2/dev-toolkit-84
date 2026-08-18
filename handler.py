import json
import requests

class CryptoAPI:
    BASE_URL = 'https://api.coingecko.com/api/v3'

    @staticmethod
    def fetch_data(endpoint, params=None):
        try:
            response = requests.get(f'{CryptoAPI.BASE_URL}/{endpoint}', params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error occurred: {e}')  # Real error logging would go here
            return None
        except Exception as e:
            print(f'An error occurred: {e}')  # General error logging
            return None

    @classmethod
    def get_crypto_price(cls, crypto_id):
        data = cls.fetch_data('simple/price', {'ids': crypto_id, 'vs_currencies': 'usd'})
        if data:
            return data.get(crypto_id, {}).get('usd', None)
        return None

    @classmethod
    def get_market_data(cls, crypto_id):
        data = cls.fetch_data(f'coins/{crypto_id}/market_chart', {'vs_currency': 'usd', 'days': '1'})
        if data:
            return data
        return None

if __name__ == '__main__':
    bitcoin_price = CryptoAPI.get_crypto_price('bitcoin')
    print('Bitcoin Price:', bitcoin_price)
    market_data = CryptoAPI.get_market_data('bitcoin')
    print('Market Data:', json.dumps(market_data, indent=2))