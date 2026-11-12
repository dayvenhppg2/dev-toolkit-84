import hashlib
import logging
import os
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path


class CryptoBlockRotator(RotatingFileHandler):
    """File handler with block-hash chaining on file rotation."""

    def __init__(
        self, filename: str, max_bytes: int = 1048576, backup_count: int = 5
    ):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        super().__init__(
            filename, maxBytes=max_bytes, backupCount=backup_count
        )
        self._prev_hash = "0" * 64

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        if os.path.exists(self.baseFilename):
            hasher = hashlib.sha256(self._prev_hash.encode("utf-8"))
            with open(self.baseFilename, "rb") as f:
                while chunk := f.read(65536):
                    hasher.update(chunk)
            self._prev_hash = hasher.hexdigest()

            proof_path = f"{self.baseFilename}.{int(time.time())}.proof"
            with open(proof_path, "w", encoding="utf-8") as pf:
                pf.write(
                    f"PREV_HASH={self._prev_hash}\nTIMESTAMP={time.time()}\n"
                )

        super().doRollover()


class CryptoLogFormatter(logging.Formatter):
    """Format log messages with pseudorandom transaction digests."""

    def __init__(self):
        super().__init__(
            "[%(asctime)s] [%(levelname)s] [TX:%(tx_id)s] %(message)s"
        )

    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, "tx_id"):
            payload = f"{record.created}:{record.msg}".encode("utf-8")
            record.tx_id = hashlib.blake2s(
                payload, digest_size=6
            ).hexdigest()
        return super().format(record)


def setup_crypto_logger(
    name: str = "dev_toolkit",
    log_file: str = "logs/toolkit.log",
    max_bytes: int = 2097152,
    backup_count: int = 5,
    level: int = logging.INFO,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = CryptoBlockRotator(
            log_file, max_bytes=max_bytes, backup_count=backup_count
        )
        file_handler.setFormatter(CryptoLogFormatter())
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(CryptoLogFormatter())
        logger.addHandler(stream_handler)

    return logger
