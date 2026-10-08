import hashlib
import logging
from logging.handlers import RotatingFileHandler
import time

class BlockchainFormatter(logging.Formatter):
    """
    A formatter that chains log entries together using SHA-256 hashes,
    creating a tamper-evident audit trail for crypto operations.
    """
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.prev_hash = "0" * 64

    def format(self, record):
        original_msg = super().format(record)
        timestamp = str(time.time())
        # Chain the current log to the previous log's hash
        payload = f"{self.prev_hash}|{timestamp}|{original_msg}"
        current_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        
        # Build output with partial hash chain visuals
        chain_tag = f"[blk:{current_hash[:8]}<-{self.prev_hash[:8]}]"
        self.prev_hash = current_hash
        return f"{chain_tag} {original_msg}"

def setup_logger(name: str, log_filepath: str = "ledger.log") -> logging.Logger:
    """Initializes a rotating logger linked cryptographically."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # Ensure we rotate at ~5MB, keeping 3 history files
        rotating_handler = RotatingFileHandler(
            log_filepath, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3,
            encoding="utf-8"
        )
        
        formatter = BlockchainFormatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        rotating_handler.setFormatter(formatter)
        logger.addHandler(rotating_handler)
        
    return logger
