import json

class InputError(Exception):
    pass

class DataHandler:
    def __init__(self, data):
        self.data = data

    def validate_input(self):
        if not isinstance(self.data, dict):
            raise InputError("Input must be a dictionary")
        if "name" not in self.data or "age" not in self.data:
            raise InputError("Required fields: name and age")
        if not isinstance(self.data["name"], str):
            raise InputError("Name must be a string")
        if not isinstance(self.data["age"], int) or self.data["age"] <= 0:
            raise InputError("Age must be a positive integer")

    def process(self):
        self.validate_input()
        processed_data = json.dumps(self.data)
        return processed_data

if __name__ == '__main__':
    user_data = {"name": "Alice", "age": 30}  
    handler = DataHandler(user_data)
    try:
        result = handler.process()
        print(result)
    except InputError as e:
        print(f"Input Error: {str(e)}")