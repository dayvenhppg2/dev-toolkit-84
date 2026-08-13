import logging

class CustomLogger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def log_performance(self, message, exec_time):
        self.logger.info(f'{message} - Execution time: {exec_time:.5f} seconds')

custom_logger = CustomLogger('CryptoLogger')

# Example usage
if __name__ == '__main__':
    import time
    start_time = time.time()
    custom_logger.info('Starting performance test')
    time.sleep(1)  # Simulate some process
    custom_logger.log_performance('Finished performance test', time.time() - start_time)