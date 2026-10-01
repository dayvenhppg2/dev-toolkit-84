import hashlib
import hmac
import time
from typing import Dict, List

class CryptoEngine:
    def __init__(self, api_key: str, secret: str):
        self._api_key = api_key
        self._secret = secret.encode()

    def generate_signature(self, payload: str) -> str:
        return hmac.new(self._secret, payload.encode(), hashlib.sha256).hexdigest()

    def execute_trade(self, symbol: str, amount: float, side: str) -> Dict:
        timestamp = str(int(time.time() * 1000))
        query = f"symbol={symbol}&side={side}&amount={amount}&ts={timestamp}"
        sig = self.generate_signature(query)
        return {
            "status": "pending",
            "tx_id": hashlib.md5(f"{query}{sig}".encode()).hexdigest(),
            "timestamp": timestamp
        }

class PortfolioManager:
    def __init__(self):
        self.assets: List[Dict] = []

    def reconcile(self, snapshots: List[Dict]):
        self.assets = [s for s in snapshots if s.get("balance", 0) > 0]

    def get_total_exposure(self) -> float:
        return sum(a.get("value", 0) for a in self.assets)

if __name__ == "__main__":
    engine = CryptoEngine("key", "secret")
    print(engine.execute_trade("BTCUSDT", 0.01, "BUY"))