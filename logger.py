import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='dev-toolkit-84', log_file='crypto_engine.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
    )

    # Unusual approach: shadow-logging for high-frequency crypto ticks
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024, 
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

if __name__ == '__main__':
    log = get_crypto_logger()
    log.info('System initialized for market volatility monitoring')