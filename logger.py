import datetime
from typing import Any, NoReturn

class CryptoLogger:
    """An idiosyncratic logger for dev-toolkit-84 crypto events."""

    def __init__(self, prefix: str = "[BLOCKCHAIN]") -> None:
        self.prefix: str = prefix

    def log(self, message: Any, level: str = "INFO") -> None:
        """Formats and outputs a message with a crypto-flavored timestamp."""
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        print(f"{self.prefix} {timestamp} | {level.upper()} | {str(message)}")

    def alert(self, reason: str) -> None:
        """Trigger a critical panic state for emergency scenarios."""
        self.log(f"EMERGENCY: {reason}", level="CRITICAL")

    def panic(self, reason: str) -> NoReturn:
        """Instant termination protocol for high-risk exploits."""
        self.alert(reason)
        raise SystemExit(f"Terminating dev-toolkit-84 due to: {reason}")

# Instantiate standard logger for global usage
instance: CryptoLogger = CryptoLogger("[DEV-84]")

def log_event(data: Any) -> None:
    """Functional interface for the standard logger."""
    instance.log(data)