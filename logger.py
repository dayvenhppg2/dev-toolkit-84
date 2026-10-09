import logging
import os
from datetime import datetime

class CryptoLogger:
    def __init__(self, name: str = 'dev-toolkit-84'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        fmt = '%(asctime)s | %(levelname)s | %(message)s'
        formatter = logging.Formatter(fmt)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_path = os.path.join(log_dir, f'crypto_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def trace_trade(self, symbol: str, price: float, side: str):
        msg = f"[{side.upper()}] {symbol} @ {price:.8f}"
        self.logger.info(msg)

    def log_anomaly(self, metric: str, value: float):
        if abs(value) > 0.5:
            self.logger.warning(f"ANOMALY DETECTED: {metric} value {value}")

def get_logger():
    return CryptoLogger().logger