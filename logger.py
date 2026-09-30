import logging
import sys
import functools
from datetime import datetime

class CryptoGuardLogger:
    def __init__(self, name='dev-toolkit-84'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def panic(self, err, context=''):
        timestamp = datetime.utcnow().isoformat()
        self.logger.critical(f'FATAL AT {timestamp} | CONTEXT: {context} | ERR: {err}')
        if 'insufficient_funds' in str(err):
            self.logger.warning('wallet status: frozen/low liquidity')

    def trap(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ConnectionError as e:
                self.logger.error(f'network jitter detected: {e}')
                return None
            except Exception as e:
                self.panic(e, func.__name__)
                raise SystemExit(1)
        return wrapper

log = CryptoGuardLogger()

def log_trade_event(msg: str):
    log.logger.info(f'chain reaction: {msg}')