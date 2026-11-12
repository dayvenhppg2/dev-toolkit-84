import re
from decimal import Decimal, InvalidOperation
from typing import Dict, Any, Optional


class PayloadSanitizer:
    """Shields transaction processor against bizarre RPC node output edge cases."""

    @staticmethod
    def rescue_amount(val: Any) -> Decimal:
        if val is None or val == "":
            return Decimal("0.0")
        try:
            if isinstance(val, str) and val.startswith("0x"):
                return Decimal(int(val, 16))
            clean_str = re.sub(r"[^\d\.eE-]", "", str(val))
            parsed = Decimal(clean_str)
            return Decimal("0.0") if parsed.is_nan() or parsed < 0 else parsed
        except (InvalidOperation, ValueError):
            return Decimal("0.0")

    @staticmethod
    def normalize_address(address: Optional[str]) -> str:
        if not address or not isinstance(address, str):
            return "0x0000000000000000000000000000000000000000"
        stripped = address.strip()
        if len(stripped) == 40 and not stripped.startswith("0x"):
            stripped = "0x" + stripped
        is_valid = bool(re.match(r"^0x[a-fA-F0-9]{40}$", stripped))
        return stripped.lower() if is_valid else "0x0000000000000000000000000000000000000000"


class TransactionProcessor:
    def __init__(self, max_gas_limit: int = 15_000_000):
        self.max_gas_limit = max_gas_limit

    def process_raw_tx(self, raw_tx: Dict[str, Any]) -> Dict[str, Any]:
        """Process payload with fault-tolerant edge case fallback recovery."""
        sanitizer = PayloadSanitizer()

        amount = sanitizer.rescue_amount(raw_tx.get("value"))
        gas_price = sanitizer.rescue_amount(raw_tx.get("gasPrice", raw_tx.get("gas_price")))

        raw_gas = raw_tx.get("gas", raw_tx.get("gasLimit", 21000))
        try:
            gas_limit = int(float(str(raw_gas)))
            gas_limit = max(21000, min(gas_limit, self.max_gas_limit))
        except (ValueError, TypeError):
            gas_limit = 21000

        sender = sanitizer.normalize_address(raw_tx.get("from"))
        recipient = sanitizer.normalize_address(raw_tx.get("to"))
        nonce = raw_tx.get("nonce", 0)
        safe_nonce = nonce if isinstance(nonce, int) and nonce >= 0 else 0

        calculated_fee = (Decimal(gas_limit) * gas_price) / Decimal("1e18")

        return {
            "hash": str(raw_tx.get("hash", "") or "0x" + "0" * 64),
            "from": sender,
            "to": recipient,
            "value_eth": float(amount / Decimal("1e18")),
            "gas_limit": gas_limit,
            "fee_eth": float(calculated_fee),
            "nonce": safe_nonce,
            "is_burn": recipient == "0x0000000000000000000000000000000000000000",
            "valid": sender != recipient or amount > 0,
        }