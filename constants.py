import json
import os

DEFAULT_CONFIG = {
    'api_key': 'your_api_key_here',
    'api_secret': 'your_api_secret_here',
    'base_currency': 'BTC',
    'trade_amount': 0.01,
    'leverage': 2,
    'exchange': 'binance',
}

CONFIG_FILE_PATH = 'config.json'

class ConfigLoader:
    def __init__(self, default_config=DEFAULT_CONFIG):
        self.config = default_config

    def load_config(self):
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH, 'r') as config_file:
                user_config = json.load(config_file)
                self.config.update(user_config)
        return self.config

config_loader = ConfigLoader()  
config = config_loader.load_config()  
