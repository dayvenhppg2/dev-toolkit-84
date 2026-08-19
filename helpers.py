import json
import requests
from datetime import datetime
def fetch_crypto_price(crypto_symbol):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_symbol}&vs_currencies=usd'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Failed to fetch data')
def format_price_data(data):
    crypto_data = {}
    for key, value in data.items():
        price = value.get('usd')
        timestamp = datetime.now().isoformat()
        crypto_data[key] = {'price': price, 'timestamp': timestamp}
    return json.dumps(crypto_data, indent=4)
def save_price_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(data)