import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name: str = 'dev-toolkit-84', log_path: str = 'crypto_ops.log') -> logging.Logger:
    """Custom logger with byte-sized rotation for volatile transaction streams."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        # Rotating every 5MB, keep 3 historical snapshots
        handler = RotatingFileHandler(
            log_path, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        
        # Unconventional but legible format for rapid log tailing
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-7s | [%(name)s] -> %(message)s',
            datefmt='%H:%M:%S'
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Fallback to console if running in dev mode
        if os.getenv('DEV_MODE') == 'true':
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            logger.addHandler(console)
            
    return logger