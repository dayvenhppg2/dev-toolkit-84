import hashlib
import logging
import os
from logging.handlers import RotatingFileHandler


class CryptoAuditFormatter(logging.Formatter):
    """Custom log formatter that attaches a SHA-256 signature to each record."""

    def format(self, record: logging.LogRecord) -> str:
        base_msg = super().format(record)
        digest = hashlib.sha256(base_msg.encode("utf-8")).hexdigest()[:8]
        return f"[SHA:{digest}] {base_msg}"


class RotatedCryptoLogger:
    """Configures a rotating logger tailored for crypto trade execution logging."""

    def __init__(
        self,
        name: str = "crypto_audit",
        log_dir: str = "logs",
        max_bytes: int = 1_048_576,
        backup_count: int = 5,
    ) -> None:
        self.name = name
        self.log_dir = log_dir
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        os.makedirs(self.log_dir, exist_ok=True)
        filepath = os.path.join(self.log_dir, f"{self.name}.log")
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            handler = RotatingFileHandler(
                filepath, maxBytes=self.max_bytes, backupCount=self.backup_count
            )
            fmt_str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
            handler.setFormatter(CryptoAuditFormatter(fmt_str))
            logger.addHandler(handler)

        return logger

    def log_trade(self, tx_hash: str, pair: str, amount: float, price: float) -> None:
        msg = f"PAIR: {pair} | AMT: {amount} | PRICE: {price} | TX: {tx_hash}"
        self.logger.info(msg)


def setup_tx_logger(name: str = "trade_audit") -> logging.Logger:
    return RotatedCryptoLogger(name=name).logger
