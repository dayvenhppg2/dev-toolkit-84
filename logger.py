import os
import re
import logging
from logging.handlers import RotatingFileHandler


class CryptoAnonymizingFormatter(logging.Formatter):
    """Custom logger formatter that redacts sensitive crypto keys and tokens."""

    PATTERNS = [
        (
            re.compile(
                r'(?i)(api[_\-]?key|secret|private[_\-]?key)["\\']?\s*[:=]\s*["\\']?([a-f0-9]{32,64})["\\']?'
            ),
            r"\1=***REDACTED***",
        ),
        (re.compile(r"\b0x[a-fA-F0-9]{64}\b"), "0x" + "*" * 60 + "MASKED"),
    ]

    def format(self, record: logging.LogRecord) -> str:
        original_msg = super().format(record)
        redacted_msg = original_msg
        for pattern, replacement in self.PATTERNS:
            redacted_msg = pattern.sub(replacement, redacted_msg)
        return redacted_msg


def setup_crypto_logger(
    name: str = "crypto_toolkit",
    log_dir: str = "logs",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 5,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures a size-rotated file logger tailored for crypto applications."""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{name}.log")

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger

    fmt_str = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    formatter = CryptoAnonymizingFormatter(fmt_str, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
