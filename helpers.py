import re
from typing import Any, Callable, Dict, Generator, List, Tuple


class CryptoInputValidator:
    """Yield-based validation engine for incoming crypto event streams."""

    ADDRESS_PATTERNS = {
        "ETH": re.compile(r"^0x[a-fA-F0-9]{40}$"),
        "BTC_LEGACY": re.compile(r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$"),
        "BTC_BECH32": re.compile(r"^(bc1)[0-9a-z]{25,39}$"),
    }

    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self._validators: List[Callable[[Dict[str, Any]], Tuple[bool, str]]] = [
            self._check_payload_shape,
            self._check_address_format,
            self._check_value_bounds,
        ]

    def _check_payload_shape(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        required = {"symbol", "target_address", "amount", "nonce"}
        missing = required - data.keys()
        return (False, f"missing fields: {missing}") if missing else (True, "OK")

    def _check_address_format(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        sym = str(data.get("symbol", "")).upper()
        addr = str(data.get("target_address", ""))
        if sym == "ETH" and not self.ADDRESS_PATTERNS["ETH"].match(addr):
            return False, f"malformed eth address: {addr}"
        if sym == "BTC" and not any(
            p.match(addr)
            for p in (
                self.ADDRESS_PATTERNS["BTC_LEGACY"],
                self.ADDRESS_PATTERNS["BTC_BECH32"],
            )
        ):
            return False, f"malformed btc address: {addr}"
        return True, "OK"

    def _check_value_bounds(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        val = data.get("amount")
        if not isinstance(val, (int, float)) or val <= 0:
            return False, f"non-positive or bad type amount: {val}"
        return True, "OK"

    def sanitize_stream(
        self, stream: List[Dict[str, Any]]
    ) -> Generator[Tuple[Dict[str, Any], bool, str], None, None]:
        for item in stream:
            is_valid, err = True, "valid"
            for check in self._validators:
                passed, msg = check(item)
                if not passed:
                    is_valid, err = False, msg
                    if self.strict_mode:
                        break
            yield item, is_valid, err
