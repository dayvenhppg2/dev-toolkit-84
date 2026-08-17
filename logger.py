import logging
import os

class Logger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def set_log_level(self, level):
        self.logger.setLevel(level)

    @staticmethod
    def log_file_exists(file_path):
        return os.path.isfile(file_path)

    def log_to_file(self, message, file_path):
        if self.log_file_exists(file_path):
            with open(file_path, 'a') as f:
                f.write(f'{message}\n')
        else:
            self.logger.error('Log file does not exist')
