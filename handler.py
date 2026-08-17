import json
import requests
from requests.exceptions import RequestException

class CryptoHandler:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, endpoint):
        url = f'{self.api_url}/{endpoint}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return self.handle_error(e, url)
        except json.JSONDecodeError:
            return {'error': 'Invalid JSON response from server'}

    def handle_error(self, error, url):
        if isinstance(error, requests.ConnectionError):
            return {'error': 'Network problem occurred', 'url': url}
        elif isinstance(error, requests.Timeout):
            return {'error': 'Request timed out', 'url': url}
        elif isinstance(error, requests.HTTPError):
            return {'error': f'HTTP error occurred: {error}', 'url': url}
        else:
            return {'error': 'An unexpected error occurred', 'details': str(error)}

# Example usage:
if __name__ == '__main__':
    handler = CryptoHandler('https://api.example.com')
    data = handler.fetch_data('crypto_prices')
    print(data)