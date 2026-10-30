import os
import re
import logging
from logging.handlers import RotatingFileHandler


class CryptoAddressMaskingFormatter(logging.Formatter):
    """Formatter that redacts potential private keys and truncates wallet addresses."""

    PRIVKEY_REGEX = re.compile(r"(?i)\b(0x)?[a-f0-9]{64}\b")
    ADDRESS_REGEX = re.compile(r"(?i)\b(0x[a-f0-9]{40})\b")

    def format(self, record: logging.LogRecord) -> str:
        original = super().format(record)
        sanitized = self.PRIVKEY_REGEX.sub("[REDACTED_SECRET_KEY]", original)

        def shorten_addr(match):
            addr = match.group(1)
            return f"{addr[:6]}...{addr[-4:]}"

        return self.ADDRESS_REGEX.sub(shorten_addr, sanitized)


def setup_crypto_logger(
    name: str = "dev_toolkit_crypto",
    log_file: str = "logs/crypto_activity.log",
    max_bytes: int = 2 * 1024 * 1024,
    backup_count: int = 5,
    level: int = logging.INFO,
) -> logging.Logger:
    """Sets up a size-rotating logger tailored for crypto dev toolkits."""
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        fmt = "%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s"
        formatter = CryptoAddressMaskingFormatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
