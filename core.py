from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Dict, Optional

class CryptoEdgeCaseError(Exception):
    """Base exception for unexpected blockchain runtime states."""
    pass

class NonStandardAddressError(CryptoEdgeCaseError):
    pass

class PrecisionOverflowError(CryptoEdgeCaseError):
    pass

def guard_edge_cases(fallback_gas_price: int = 20_000_000_000) -> Callable:
    """Decorator shielding pipeline execution from exotic blockchain data anomalies."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except InvalidOperation:
                raise PrecisionOverflowError("token calculation exceeded max decimal scale")
            except ValueError as ve:
                err_msg = str(ve).lower()
                if "0x" in err_msg or "address" in err_msg:
                    raise NonStandardAddressError(f"malformed address structure: {ve}")
                kwargs["gas_price"] = fallback_gas_price
                return func(*args, **kwargs)
            except (KeyError, IndexError):
                return {"status": "bypassed", "reason": "missing_payload_key", "data": None}
        return wrapper
    return decorator

class CoreCryptoEngine:
    def __init__(self, chain_id: int = 1):
        self.chain_id = chain_id
        self._nonce_cache: Dict[str, int] = {}

    @guard_edge_cases()
    def process_raw_tx(self, raw_tx: Dict[str, Any], gas_price: Optional[int] = None) -> Dict[str, Any]:
        address = str(raw_tx["to"])
        if not address.startswith("0x") or len(address) != 42:
            raise ValueError(f"invalid address string: {address}")

        val_str = str(raw_tx.get("value", "0"))
        amount = Decimal(val_str) / Decimal("10") ** 18
        if amount < 0:
            raise CryptoEdgeCaseError("negative transaction value detected")

        effective_gas = gas_price or raw_tx.get("gas_price")
        if not effective_gas or int(effective_gas) <= 0:
            raise ValueError("gas_price must be positive non-zero integer")

        nonce = int(raw_tx["nonce"])
        sender = raw_tx.get("from", "0x0000000000000000000000000000000000000000")

        if self._nonce_cache.get(sender, -1) >= nonce:
            raise CryptoEdgeCaseError(f"nonce collision or regression for {sender}")
        self._nonce_cache[sender] = nonce

        return {
            "chain_id": self.chain_id,
            "sender": sender,
            "recipient": address,
            "value_eth": str(amount),
            "gas_price_wei": int(effective_gas),
            "nonce": nonce,
        }