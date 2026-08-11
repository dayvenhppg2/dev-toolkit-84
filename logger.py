import logging

class CustomLogger:
    """A custom logger for application logging."

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        """Initialize the logger with a name and level."
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create a console handler and set level to debug
        ch: logging.StreamHandler = logging.StreamHandler()
        ch.setLevel(level)

        # Create a formatter and add it to the handler
        formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(ch)

    def debug(self, message: str) -> None:
        """Log a debug message."
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log an info message."
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning message."
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message."
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Log a critical message."
        self.logger.critical(message)