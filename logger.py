import sys
import time
import inspect
from datetime import datetime

class CryptoLogger:
    COLORS = {"INFO": "\033[94m", "WARN": "\033[93m", "ERROR": "\033[91m", "SUCCESS": "\033[92m"}
    RESET = "\033[0m"

    def __init__(self, tag="DEV-84"):
        self.tag = tag

    def _format(self, level, msg):
        ts = datetime.utcnow().strftime("%H:%M:%S.%f")[:-3]
        caller = inspect.stack()[2].function
        return f"{self.COLORS.get(level, '')}[{ts}][{self.tag}][{caller}] {level}: {msg}{self.RESET}"

    def info(self, msg):
        print(self._format("INFO", msg))

    def warn(self, msg):
        print(self._format("WARN", msg), file=sys.stderr)

    def error(self, msg):
        print(self._format("ERROR", msg), file=sys.stderr)

    def success(self, msg):
        print(self._format("SUCCESS", msg))

def log_performance(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[PERF] {func.__name__} executed in {elapsed:.6f}s")
        return res
    return wrapper