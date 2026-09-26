import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name: str = 'dev-toolkit-84'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(module)s] -> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    file_path = os.path.join(log_dir, f'{name}.log')
    handler = RotatingFileHandler(
        file_path, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

logger = get_crypto_logger()