import json
import os

class ConfigLoader:
    def __init__(self, default_config: dict):
        self.default_config = default_config
        self.config = self.load_config()

    def load_config(self):
        config_path = os.getenv('CONFIG_PATH', 'config.json')
        if os.path.isfile(config_path):
            with open(config_path, 'r') as file:
                user_config = json.load(file)
            return {**self.default_config, **user_config}
        return self.default_config

    def get(self, key, default=None):
        return self.config.get(key, default)

# Usage example
def main():
    default_settings = {
        'api_key': 'your_default_api_key',
        'timeout': 30,
    }
    config_loader = ConfigLoader(default_settings)
    print(config_loader.get('api_key'))

if __name__ == '__main__':
    main()