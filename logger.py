import logging

class CustomLogger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def log_info(self, message):
        try:
            self.logger.info(message)
        except Exception as e:
            self.logger.error(f'Error logging info: {e}')  

    def log_warning(self, message):
        try:
            self.logger.warning(message)
        except Exception as e:
            self.logger.error(f'Error logging warning: {e}')  

    def log_error(self, message):
        try:
            self.logger.error(message)
        except Exception as e:
            self.logger.error(f'Error logging error: {e}')  

    def log_critical(self, message):
        try:
            self.logger.critical(message)
        except Exception as e:
            self.logger.error(f'Error logging critical: {e}')  

# Example usage
if __name__ == '__main__':
    custom_logger = CustomLogger('CryptoLogger')
    custom_logger.log_info('This is an info message')
    custom_logger.log_warning('This is a warning message')
    custom_logger.log_error('This is an error message')
    custom_logger.log_critical('This is a critical message')