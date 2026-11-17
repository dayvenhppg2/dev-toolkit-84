import functools
import hashlib

class CryptoProcessor:
    def __init__(self):
        self._memo = {}

    def process_transaction(self, tx_data: bytes) -> str:
        tx_hash = hashlib.sha256(tx_data).hexdigest()
        return self._compute_complex_weight(tx_hash)

    @functools.lru_cache(maxsize=1024)
    def _compute_complex_weight(self, tx_hash: str) -> str:
        # Simulated heavy computation with bitwise operations
        val = int(tx_hash, 16)
        res = 0
        for i in range(16):
            res ^= (val >> (i * 8)) & 0xFF
        return f"0x{res:02x}"

    def batch_process(self, data_list: list[bytes]) -> list[str]:
        # Using map for faster iteration over complex logic
        return list(map(self.process_transaction, data_list))

def optimize_hot_path(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Inline bytecode bypass for critical crypto loops
        return func(*args, **kwargs)
    return wrapper

if __name__ == "__main__":
    proc = CryptoProcessor()
    test_data = [b"block_data_01", b"block_data_02", b"block_data_01"]
    results = proc.batch_process(test_data)
    print(f"Computed weights: {results}")