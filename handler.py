import hashlib
import hmac
from typing import Any, Callable, Dict, Literal, Optional, Tuple, TypeGuard, Union


class CryptoPayload(dict):
    """A dictionary-backed cryptographic payload container supporting pipeline execution."""

    def __init__(
        self, data: Dict[str, Any], signature: Optional[str] = None
    ) -> None:
        super().__init__(data)
        self.signature = signature

    def __ror__(
        self,
        transformer: Callable[["CryptoPayload"], "CryptoPayload"],
    ) -> "CryptoPayload":
        """Allows piping transformers using the bitwise OR operator."""
        return transformer(self)


def is_valid_tx_payload(
    payload: Dict[str, Any]
) -> TypeGuard[Dict[str, Union[str, int]]]:
    """TypeGuard validating that a dictionary conforms to expected transaction payload keys."""
    required_keys = {"tx_hash", "amount", "sender", "receiver"}
    if not required_keys.issubset(payload.keys()):
        return False
    return isinstance(payload["tx_hash"], str) and isinstance(
        payload["amount"], int
    )


class PayloadHandler:
    """Dispatches and decorates incoming cryptographic payload events with HMAC signatures."""

    def __init__(
        self, secret_key: bytes, algorithm: Literal["sha256", "sha512"] = "sha256"
    ) -> None:
        self._secret = secret_key
        self._algo = getattr(hashlib, algorithm)

    def sign(self, payload: CryptoPayload) -> CryptoPayload:
        """Computes and attaches an HMAC signature to the payload."""
        serialized = "&".join(
            f"{k}={v}" for k, v in sorted(payload.items())
        ).encode("utf-8")
        sig = hmac.new(self._secret, serialized, self._algo).hexdigest()
        payload.signature = sig
        return payload

    def verify(self, payload: CryptoPayload) -> bool:
        """Verifies the HMAC signature attached to a payload."""
        if not payload.signature:
            return False
        expected = self.sign(CryptoPayload(dict(payload))).signature
        return hmac.compare_digest(payload.signature, expected or "")

    def process(self, raw_data: Dict[str, Any]) -> Tuple[bool, CryptoPayload]:
        """Ingests raw transaction data, verifies schema integrity, and signs the payload."""
        if not is_valid_tx_payload(raw_data):
            raise ValueError("Malformed cryptographic transaction payload")

        payload = CryptoPayload(raw_data)
        signed_payload = payload | self.sign
        is_verified = self.verify(signed_payload)
        return is_verified, signed_payload
