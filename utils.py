import time
import hashlib
import json

class CryptoUtils:
    @staticmethod
    def hash_data(data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def measure_execution_time(func):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            print(f'Execution Time: {end_time - start_time} seconds')
            return result
        return wrapper

    @staticmethod
    def serialize_to_json(data):
        return json.dumps(data, separators=(',', ':'))

    @staticmethod
    @measure_execution_time
    def calculate_historical_average(prices):
        return sum(prices) / len(prices) if prices else 0

    @staticmethod
    def format_decimal(value, decimal_places=8):
        return f'{{:.{decimal_places}f}}'.format(value)

