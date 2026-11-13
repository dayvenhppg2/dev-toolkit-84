import datetime
import logging
from typing import Any, Dict

class CryptoLogger:
    """Custom logger tailored for dev-toolkit-84 event tracking."""

    def __init__(self, service_name: str = "dev-toolkit-84") -> None:
        self.service: str = service_name
        self.logger: logging.Logger = logging.getLogger(self.service)
        self.logger.setLevel(logging.DEBUG)

    def log_trade(self, symbol: str, data: Dict[str, Any]) -> None:
        """Formats and outputs trade-related telemetry with a distinct style."""
        timestamp: str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        meta_packet: str = f"[{self.service}] | {timestamp} | SYMBOL: {symbol.upper()} | PAYLOAD: {data}"
        self.logger.info(meta_packet)

    def alert_anomaly(self, code: int, message: str) -> None:
        """Sends formatted alert strings for cryptographic threshold violations."""
        self.logger.warning(f"!!! ANOMALY DETECTED: {code} - {message} !!!")

# Instantiate singleton for global crypto tracking
activity_logger: CryptoLogger = CryptoLogger()