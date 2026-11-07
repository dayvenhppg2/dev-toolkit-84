import sys
import math
from typing import Any, Callable, TypeVar
from functools import wraps

T = TypeVar("T")

class CryptoEdgeCaseError(Exception):
    """Base exception for unexpected telemetry and transaction anomalies."""
    def __init__(self, message: str, raw_payload: Any = None, recovery_hint: str = ""):
        super().__init__(message)
        self.raw_payload = raw_payload
        self.recovery_hint = recovery_hint

class ResilientPayloadHandler:
    def __init__(self, max_satoshis: int = 21_000_000 * 10**8):
        self.max_satoshis = max_satoshis

    def sanitize_hex_sig(self, hex_str: Any) -> str:
        """Edge case: handle non-string, unprefixed, odd-length, or padded hex signatures."""
        if not isinstance(hex_str, (str, bytes)):
            raise CryptoEdgeCaseError("Signature payload is non-bytes/str", raw_payload=hex_str, recovery_hint="cast_to_string")
        
        cleaned = hex_str.decode("utf-8") if isinstance(hex_str, bytes) else hex_str
        cleaned = cleaned.strip().lower()
        if cleaned.startswith("0x"):
            cleaned = cleaned[2:]
        
        if len(cleaned) % 2 != 0:
            cleaned = "0" + cleaned
            
        if not all(c in "0123456789abcdef" for c in cleaned):
            raise CryptoEdgeCaseError("Invalid characters in hex signature", raw_payload=hex_str)
            
        return f"0x{cleaned}"

    def safe_parse_amount(self, raw_val: Any, fallback: int = 0) -> int:
        """Edge case: float NaNs, negative amounts, scientific strings, string floats."""
        try:
            if isinstance(raw_val, float):
                if math.isnan(raw_val) or math.isinf(raw_val):
                    return fallback
                val = int(raw_val)
            elif isinstance(raw_val, str):
                cleaned_str = raw_val.strip()
                if "." in cleaned_str or "e" in cleaned_str.lower():
                    val = int(float(cleaned_str))
                else:
                    val = int(cleaned_str)
            else:
                val = int(raw_val)

            if val < 0 or val > self.max_satoshis:
                return fallback
            return val
        except (ValueError, TypeError, OverflowError):
            return fallback

def edge_fault_shield(default_factory: Callable[[], Any]):
    """Decorator wrapping crypto telemetry routines against unexpected execution panics."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except CryptoEdgeCaseError as err:
                sys.stderr.write(f"[SHIELD TRAP] Managed payload fault: {err} | Hint: {err.recovery_hint}\n")
                return default_factory()
            except (KeyError, IndexError, ZeroDivisionError) as err:
                sys.stderr.write(f"[SHIELD TRAP] Structural failure intercepted: {type(err).__name__}\n")
                return default_factory()
        return wrapper
    return decorator