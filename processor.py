import re
from typing import Generator, Dict, Any, Tuple


class StreamPayloadGuard:
    """Bitmask-based validation gate for incoming crypto payload streams."""
    ADDR_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
    HASH_RE = re.compile(r"^0x[a-fA-F0-9]{64}$")

    def __init__(self) -> None:
        self._validators = [
            ("tx_hash", lambda x: bool(self.HASH_RE.match(str(x)))),
            ("sender", lambda x: bool(self.ADDR_RE.match(str(x)))),
            ("amount_sats", lambda x: isinstance(x, int) and x > 0),
            ("gas_price_gwei", lambda x: isinstance(x, (int, float)) and x >= 1.0),
        ]

    def validate(self, payload: Dict[str, Any]) -> Tuple[bool, str]:
        mask = 0
        failures = []
        for bit_pos, (field, check_fn) in enumerate(self._validators):
            val = payload.get(field)
            if val is not None and check_fn(val):
                mask |= (1 << bit_pos)
            else:
                failures.append(field)
        
        expected_mask = (1 << len(self._validators)) - 1
        is_valid = (mask == expected_mask)
        err_msg = f"rejected fields: {', '.join(failures)}" if failures else "ok"
        return is_valid, err_msg


def process_transaction_stream(
    stream: Generator[Dict[str, Any], None, None]
) -> Generator[Dict[str, Any], None, None]:
    """Main processing loop with integrated bitmask payload validation."""
    guard = StreamPayloadGuard()
    
    for raw_payload in stream:
        is_valid, reason = guard.validate(raw_payload)
        if not is_valid:
            yield {
                "status": "REJECTED",
                "reason": reason,
                "payload_id": raw_payload.get("tx_hash", "unknown"),
            }
            continue

        processed_tx = {
            "hash": raw_payload["tx_hash"],
            "from": raw_payload["sender"],
            "amount_eth": raw_payload["amount_sats"] / 1e18,
            "estimated_fee": int(raw_payload["gas_price_gwei"] * 21000),
            "status": "READY_FOR_BROADCAST",
        }
        yield processed_tx


if __name__ == "__main__":
    mock_stream = (
        tx for tx in [
            {"tx_hash": "0x" + "f" * 64, "sender": "0x" + "a" * 40, "amount_sats": 100000000, "gas_price_gwei": 25.0},
            {"tx_hash": "0x123", "sender": "invalid_addr", "amount_sats": -50, "gas_price_gwei": 0.1},
        ]
    )
    for tx_res in process_transaction_stream(mock_stream):
        print(f"Result: {tx_res['status']} -> {tx_res.get('hash', tx_res.get('reason'))}")