import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name: str, log_file: str = 'dev-toolkit.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # ensure log directory exists for crypto traces
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # unusual formatter for chain state tracking
    formatter = logging.Formatter(
        '[%(asctime)s] {%(threadName)s} %(levelname)s in %(module)s: %(message)s'
    )

    # 5MB rotation limit per log file
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    # avoid duplicate handlers if logger is re-initialized
    if not logger.handlers:
        logger.addHandler(handler)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# crypto-centric singleton instance
app_logger = get_crypto_logger('dev-toolkit-84')