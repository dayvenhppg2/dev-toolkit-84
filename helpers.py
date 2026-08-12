import hashlib
import json
import requests

def generate_hash(data):
    serialized_data = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(serialized_data).hexdigest()


def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Error fetching data: {e}')
        return None


def validate_signature(data, provided_signature, secret):
    hash = generate_hash(data)
    expected_signature = hashlib.sha256((hash + secret).encode('utf-8')).hexdigest()
    return expected_signature == provided_signature


def format_timestamp(timestamp):
    from datetime import datetime
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')