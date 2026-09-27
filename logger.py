import logging
from logging.handlers import RotatingFileHandler
import os

class CryptoLogger:
    def __init__(self, log_file='dev-toolkit-84.log'):
        self.logger = logging.getLogger('crypto_engine')
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '[%(asctime)s] | %(levelname)s | %(message)s', 
            datefmt='%Y-%m-%dT%H:%M:%S'
        )

        handler = RotatingFileHandler(
            log_file, 
            maxBytes=1048576, 
            backupCount=5
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger

def setup_crypto_logging():
    return CryptoLogger().get_logger()

if __name__ == '__main__':
    log = setup_crypto_logging()
    log.info('init crypto runtime environment')