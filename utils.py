import time
import functools
import logging

logger = logging.getLogger("dev-toolkit-84")

def retry_crypto_op(retries=3, delay=1.5, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries:
                        logger.critical(f"Crypto operation '{func.__name__}' failed after {retries} attempts: {e}")
                        raise
                    logger.warning(f"Attempt {attempt} failed for '{func.__name__}': {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_crypto_op(retries=4, delay=1.0)
def broadcast_transaction(tx_hex: str) -> str:
    import random
    if random.random() < 0.7:
        raise ConnectionError("Mempool congestion / peer timeout")
    return f"tx_hash_{tx_hex[:8]}"
