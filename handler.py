import json
import requests

class CryptoHandler:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_data(self, endpoint, params=None):
        response = requests.get(f'{self.base_url}/{endpoint}', params=params)
        response.raise_for_status()
        return response.json()

    def get_price(self, crypto_id):
        data = self.fetch_data('simple/price', {'ids': crypto_id, 'vs_currencies': 'usd'})
        return data[crypto_id]['usd']

    def get_market_cap(self, crypto_id):
        data = self.fetch_data('coins/markets', {'vs_currency': 'usd', 'ids': crypto_id})
        return data[0]['market_cap'] if data else None

    def get_price_history(self, crypto_id, days):
        data = self.fetch_data('coins/' + crypto_id + '/market_chart', {'vs_currency': 'usd', 'days': days})
        return data['prices']

# Example usage:
# handler = CryptoHandler('https://api.coingecko.com/api/v3')
# price = handler.get_price('bitcoin')
# market_cap = handler.get_market_cap('bitcoin')
# history = handler.get_price_history('bitcoin', 30)