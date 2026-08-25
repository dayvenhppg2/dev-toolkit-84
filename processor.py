import hashlib
import json
from typing import List, Dict, Any, Optional

class CryptoProcessor:
    def __init__(self) -> None:
        self.processed = 0
        self.errors = []

    def validate_private_key(self, key: str) -> bool:
        if not isinstance(key, str):
            return False
        if len(key) != 64:
            return False
        try:
            int(key, 16)
            return key != "0" * 64
        except ValueError:
            return False

    def process_transaction(self, tx: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            if not tx or not isinstance(tx, dict):
                raise ValueError("Transaction data must be a non-empty dict")
            amount = tx.get("amount")
            if amount is None or not isinstance(amount, (int, float)) or amount <= 0:
                raise ValueError("Amount must be positive number")
            address = tx.get("address", "")
            if not isinstance(address, str) or len(address) < 26:
                raise ValueError("Invalid crypto address format")
            priv_key = tx.get("private_key", "")
            if not self.validate_private_key(priv_key):
                raise ValueError("Invalid or zero private key")
            tx_str = json.dumps(tx, sort_keys=True)
            tx_id = hashlib.sha256(tx_str.encode()).hexdigest()
            self.processed += 1
            return {"tx_id": tx_id, "amount": amount, "address": address[:10] + "..."}

        except ValueError as ve:
            self.errors.append(f"Validation error: {ve}")
            return None
        except TypeError as te:
            self.errors.append(f"Type error: {te}")
            return None
        except Exception as e:
            self.errors.append(f"Unexpected error: {e}")
            return None

    def process_batch(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []
        for i, tx in enumerate(transactions):
            try:
                result = self.process_transaction(tx)
                if result:
                    results.append(result)
                else:
                    results.append({"index": i, "status": "failed"})
            except Exception as e:
                self.errors.append(f"Batch processing failed at {i}: {e}")
                results.append({"index": i, "status": "error"})
        return {
            "results": results,
            "processed_count": self.processed,
            "error_count": len(self.errors),
            "errors": self.errors
        }
