import logging
import os
from datetime import datetime

class CryptoLogger:
    def __init__(self, name='dev-toolkit-84'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '[%(asctime)s] | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def entry(self, level, msg, tags=None):
        tag_str = f"[{'|'.join(tags)}] " if tags else ""
        full_msg = f"{tag_str}{msg}"
        getattr(self.logger, level.lower())(full_msg)

    @staticmethod
    def audit_trail(data, filename='audit.log'):
        with open(filename, 'a') as f:
            f.write(f"{datetime.utcnow().isoformat()}Z | {data}\n")

def get_logger():
    return CryptoLogger()

log = get_logger()