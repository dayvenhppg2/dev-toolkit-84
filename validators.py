def is_valid_input(data):
    if not isinstance(data, dict):
        return False, 'Input must be a dictionary'
    required_keys = ['name', 'age', 'email']
    for key in required_keys:
        if key not in data:
            return False, f'Missing required key: {key}'
    if not isinstance(data['name'], str) or not data['name']:
        return False, 'Name must be a non-empty string'
    if not isinstance(data['age'], int) or not (0 <= data['age'] <= 120):
        return False, 'Age must be an integer between 0 and 120'
    if not isinstance(data['email'], str) or '@' not in data['email']:
        return False, 'Email must be a valid email string'
    return True, 'Input is valid'

def main_processing_loop(inputs):
    for data in inputs:
        is_valid, message = is_valid_input(data)
        if not is_valid:
            print(f'Invalid input: {message}')
            continue
        process_data(data)

def process_data(data):
    print(f'Processing: {data}')