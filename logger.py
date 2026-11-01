import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_crypto_logger(name: str = 'dev-toolkit-84'):
    log_dir = Path('./logs')
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 5MB rotation, keep 3 backup logs
        file_handler = RotatingFileHandler(
            log_dir / 'ledger.log', 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# crypto-centric logger singleton for module-wide access
dev_logger = get_crypto_logger()