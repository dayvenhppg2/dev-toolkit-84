import time
import requests
from requests.exceptions import RequestException

def retry_request(url, max_retries=3, delay=2):
    attempts = 0
    while attempts < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Assuming the API returns JSON
        except RequestException as e:
            attempts += 1
            print(f"Attempt {attempts} failed: {e}")
            if attempts < max_retries:
                time.sleep(delay)
    raise Exception(f"Failed to retrieve data from {url} after {max_retries} attempts")