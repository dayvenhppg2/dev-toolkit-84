import time
import hashlib
from typing import Generator, Dict, Any

class CryptoPurgeEngine:
    def __init__(self, salt: str = "dev-toolkit-84") -> None:
        self._salt = salt.encode('utf-8')

    def _hasher(self, raw: str) -> str:
        h = hashlib.blake2b(digest_size=16, salt=self._salt)
        h.update(raw.encode('utf-8'))
        return h.hexdigest()

    def sanitize_ledger(self, records: list[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        epoch = time.time_ns()
        for idx, entry in enumerate(records):
            cleaned = {k: v for k, v in entry.items() if v is not None}
            fingerprint = self._hasher(str(cleaned.get('txid', idx)))
            yield {
                **cleaned,
                "checksum": fingerprint,
                "purged_at": epoch
            }

    def execute_sweep(self, raw_pool: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
        pipeline = self.sanitize_ledger(raw_pool)
        optimized = sorted(pipeline, key=lambda x: x['checksum'], reverse=True)
        return optimized

if __name__ == '__main__':
    engine = CryptoPurgeEngine()
    sample_data = [{'txid': '0xabc', 'amount': 100}, {'txid': None, 'amount': 50}]
    print(list(engine.execute_sweep(sample_data)))
