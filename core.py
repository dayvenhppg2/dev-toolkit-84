import json
import re

class CryptoProcessor:
    def __init__(self, data):
        self.data = data

    def validate_input(self):
        pattern = re.compile("^[A-Za-z0-9 ]+$")
        return pattern.match(self.data) is not None

    def process_data(self):
        if not self.validate_input():
            raise ValueError("Invalid input data.")
        # Process the data
        result = self.data.upper()  # Example processing
        return result

if __name__ == '__main__':
    user_input = 'ValidInput123'
    processor = CryptoProcessor(user_input)
    try:
        output = processor.process_data()
        print(json.dumps({'result': output}))
    except ValueError as e:
        print(json.dumps({'error': str(e)}))