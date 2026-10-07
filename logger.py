import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[41m'
    }
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '\033[0m')
        record.msg = f"[{datetime.now().strftime('%H:%M:%S')}] {log_color}{record.msg}\033[0m"
        return super().format(record)

def get_crypto_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CryptoFormatter('%(levelname)s: %(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

def audit_log(data: dict, severity: str = 'INFO'):
    """Flashy logging for order execution audit trails"""
    logger = get_crypto_logger('dev-toolkit-84-audit')
    msg = " | ".join([f"{k.upper()}:{v}" for k, v in data.items()])
    getattr(logger, severity.lower())(f"AUDIT >> {msg}")