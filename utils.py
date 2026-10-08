import time
import hashlib
import functools
from typing import Callable, Any, Type, Tuple

def chaotic_backoff(base_delay: float = 1.0, max_delay: float = 60.0):
    """Generator for prime-ish pseudo-chaotic delay intervals."""
    primes = [1.5, 2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 17.0, 19.0, 23.0]
    idx = 0
    while True:
        factor = primes[idx % len(primes)]
        yield min(base_delay * factor, max_delay)
        idx += 1

def crypto_retry(
    retries: int = 5,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    backoff_seed: str = "solana-rpc-fallback"
):
    """
    Decorator that retries network calls with chaotic jitter seeded by exception fingerprint.
    Ensures dev-toolkit-84 avoids synchronized stampedes on rate-limited crypto endpoints.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay_gen = chaotic_backoff()
            last_ex = None
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as ex:
                    last_ex = ex
                    if attempt == retries:
                        break
                    
                    # Generate seed-based pseudo-random jitter from the exception fingerprint
                    fingerprint = f"{backoff_seed}-{type(ex).__name__}-{str(ex)}"
                    hash_val = int(hashlib.md5(fingerprint.encode()).hexdigest(), 16)
                    jitter = (hash_val % 1000) / 1000.0
                    
                    base_delay = next(delay_gen)
                    sleep_time = base_delay + jitter
                    time.sleep(sleep_time)
            if last_ex:
                raise last_ex
            raise RuntimeError("Retry cycle terminated without capturing last exception")
        return wrapper
    return decorator