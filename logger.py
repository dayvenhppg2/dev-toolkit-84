import logging
from logging.handlers import RotatingFileHandler
import os

class CryptoLogger:
    def __init__(self, name='dev-toolkit-84', log_file='crypto.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(module)s.%(funcName)s:%(lineno)d | %(message)s'
        )
        
        # 5MB rotation, keep 3 historical logs
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
        
        # Console stream for dev visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get(self):
        return self.logger

# Instantiate singleton for toolkit-wide access
logger = CryptoLogger().get()

if __name__ == '__main__':
    logger.info('crypto engine initialized')