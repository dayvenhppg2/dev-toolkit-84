import json
import requests

class CryptoProcessor:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, crypto_symbol):
        response = requests.get(f'{self.api_url}/{crypto_symbol}')
        if response.status_code != 200:
            raise ValueError('Error fetching data')
        return response.json()

    def process_data(self, data):
        price = data.get('price')
        volume = data.get('volume')
        if price is None or volume is None:
            raise ValueError('Invalid data structure')
        return {'price': price, 'volume': volume}

    def run(self, crypto_symbol):
        raw_data = self.fetch_data(crypto_symbol)
        return self.process_data(raw_data)

if __name__ == '__main__':
    processor = CryptoProcessor(api_url='https://api.example.com/crypto')
    result = processor.run('BTC')
    print(json.dumps(result, indent=4))