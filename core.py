import requests
import time

class NetworkError(Exception):
    pass

def retry_request(url, retries=3, delay=1, backoff=2):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()  # assuming response is JSON
        except requests.RequestException as e:
            attempt += 1
            if attempt == retries:
                raise NetworkError(f'Failed after {retries} attempts: {e}')
            time.sleep(delay)
            delay *= backoff  # increase the delay exponentially

if __name__ == '__main__':
    url = 'https://api.example.com/data'
    try:
        data = retry_request(url)
        print(data)
    except NetworkError as ne:
        print(ne)