import logging

class CustomLogger:
    """
    A custom logger for handling log messages in a standardized way.
    """
    def __init__(self, module_name: str) -> None:
        """
        Initializes the logger with a specified module name.
        """
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def debug(self, message: str) -> None:
        """
        Logs a debug message.
        """
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """
        Logs an info message.
        """
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """
        Logs a warning message.
        """
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """
        Logs an error message.
        """
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """
        Logs a critical message.
        """
        self.logger.critical(message)

logger = CustomLogger(__name__)