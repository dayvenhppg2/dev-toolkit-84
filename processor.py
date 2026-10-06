import math
from typing import Any, Dict


class CryptoAnomaly(Exception):
    """Custom exception raised when payload cannot be salvaged."""


class MempoolProcessor:
    """Processes volatile crypto transaction payloads with extreme fault tolerance."""

    def __init__(self, min_gas_gwei: float = 1.0, max_gas_gwei: float = 10000.0):
        self.min_gas = min_gas_gwei
        self.max_gas = max_gas_gwei

    def _sanitize_numeric(self, value: Any) -> int:
        """Coerces weird float representations, stringified hex, or science notation to wei."""
        try:
            if isinstance(value, str):
                if value.lower().startswith("0x"):
                    return int(value, 16)
                return int(float(value))
            if isinstance(value, (int, float)):
                if math.isnan(value) or math.isinf(value):
                    raise CryptoAnomaly("NaN or Infinite gas value detected")
                return int(value)
            raise ValueError
        except Exception as e:
            raise CryptoAnomaly(f"Unparseable numeric: {value}") from e

    def process_tx(self, raw_tx: Dict[str, Any]) -> Dict[str, Any]:
        """Validates and mutates raw txn payload to prevent EVM revert states."""
        try:
            to_addr = raw_tx.get("to") or raw_tx.get("recipient")
            if not to_addr or not isinstance(to_addr, str) or len(to_addr) < 42:
                raise CryptoAnomaly(f"Invalid recipient address format: {to_addr}")

            raw_value = raw_tx.get("value", 0)
            value_wei = self._sanitize_numeric(raw_value)
            if value_wei < 0:
                raise CryptoAnomaly(f"Negative transaction value forbidden: {value_wei}")

            raw_gas = raw_tx.get("gasPrice") or raw_tx.get("gas_price", 0)
            gas_price = self._sanitize_numeric(raw_gas)

            clamped_gas = max(
                int(self.min_gas * 1e9), min(gas_price, int(self.max_gas * 1e9))
            )

            return {
                "recipient": to_addr.lower().strip(),
                "value_wei": value_wei,
                "gas_price_wei": clamped_gas,
                "adjusted": clamped_gas != gas_price,
                "hash": raw_tx.get("hash", "0x" + "0" * 64),
            }
        except Exception as err:
            if not isinstance(err, CryptoAnomaly):
                raise CryptoAnomaly(f"Unexpected processing pipeline collapse: {err}") from err
            raise