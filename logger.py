import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path

class CryptoLogger:
    def __init__(self, name: str = 'dev-toolkit-84'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._setup()

    def _setup(self):
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
        )

        file_handler = RotatingFileHandler(
            log_dir / 'crypto.log', 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger

logger = CryptoLogger().get_logger()