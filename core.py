import functools
import logging
import time

class CryptoCircuitBreaker:
    def __init__(self, limit=3):
        self.failures = 0
        self.limit = limit
        self.last_reset = time.time()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.failures >= self.limit:
                if time.time() - self.last_reset > 60:
                    self.failures = 0
                else:
                    raise ConnectionError("Circuit open: too many crypto-node failures")
            try:
                result = func(*args, **kwargs)
                self.failures = max(0, self.failures - 1)
                return result
            except Exception as e:
                self.failures += 1
                self.last_reset = time.time()
                logging.error(f"Node heartbeat failure: {e}")
                raise
        return wrapper

@CryptoCircuitBreaker(limit=2)
def execute_trade(pair: str, amount: float):
    if amount <= 0:
        raise ValueError("insufficient liquidity for trade")
    return {"status": "success", "pair": pair, "txid": "0xdeadbeef"}

if __name__ == "__main__":
    try:
        print(execute_trade("BTC/USD", 0.5))
        execute_trade("ETH/USD", -1.0)
    except Exception as err:
        print(f"Critical path interrupted: {err}")