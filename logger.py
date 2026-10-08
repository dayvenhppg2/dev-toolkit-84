import logging
import os
from datetime import datetime

class CryptoLogger:
    def __init__(self, name: str = 'dev-toolkit-84'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        self._setup_handlers()

    def _setup_handlers(self):
        console = logging.StreamHandler()
        console.setFormatter(self.formatter)
        self.logger.addHandler(console)
        
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        fh = logging.FileHandler(f"{log_dir}/crypto_{datetime.now().strftime('%Y%m%d')}.log")
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

    def audit(self, trade_data: dict, status: str = 'INFO'):
        log_msg = f"TRADE_AUDIT | ID:{trade_data.get('id')} | SYMBOL:{trade_data.get('pair')} | VOL:{trade_data.get('amount')}"
        if status == 'CRITICAL':
            self.logger.critical(f"!!! {log_msg} !!!")
        else:
            self.logger.info(log_msg)

    def __getattr__(self, name):
        return getattr(self.logger, name)