import json
import requests
from datetime import datetime, timedelta

class CryptoDataHandler:
    API_URL = 'https://api.coingecko.com/api/v3'

    @staticmethod
    def fetch_price(crypto_id: str) -> dict:
        response = requests.get(f'{CryptoDataHandler.API_URL}/simple/price?ids={crypto_id}&vs_currencies=usd')
        response.raise_for_status()
        return response.json()

    @staticmethod
    def historical_data(crypto_id: str, days: int) -> list:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        response = requests.get(f'{CryptoDataHandler.API_URL}/coins/{crypto_id}/market_chart/range?vs_currency=usd&from={int(start_date.timestamp())}&to={int(end_date.timestamp())}')
        response.raise_for_status()
        return response.json()['prices']

    @staticmethod
    def price_to_json(price_data: dict) -> str:
        return json.dumps(price_data, indent=4)

    @staticmethod
    def historical_to_json(historical_data: list) -> str:
        return json.dumps(historical_data, indent=4)