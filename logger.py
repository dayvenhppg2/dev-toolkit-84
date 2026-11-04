import logging
from logging.handlers import RotatingFileHandler
import sys

class CryptoLogger:
    def __init__(self, name='dev-toolkit-84', path='node.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [TXN_ID: %(process)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = RotatingFileHandler(
            path, 
            maxBytes=10*1024*1024, 
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def get_instance(self):
        return self.logger

def setup_logging(name='dev-toolkit-84', path='node.log'):
    return CryptoLogger(name, path).get_instance()

# Usage initialization
log = setup_logging()