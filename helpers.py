import requests
import json
from datetime import datetime, timedelta

class CryptoDataHandler:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, symbol, days=1):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        response = requests.get(f'{self.api_url}/historical/{symbol}', params={'start': start_date.isoformat(), 'end': end_date.isoformat()})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Error fetching data: ' + response.text)

    def parse_data(self, data):
        parsed_data = []
        for entry in data['prices']:
            timestamp, price = entry
            parsed_data.append({'date': self._format_date(timestamp), 'price': price})
        return parsed_data

    def _format_date(self, timestamp):
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')

    def save_to_file(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)

handler = CryptoDataHandler('https://api.coingecko.com/api/v3')
# an example use-case could be executed in another part of the application
