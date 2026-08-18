import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='app.log', max_bytes=5 * 1024 * 1024, backup_count=3):
    logger = logging.getLogger('CryptoLogger')
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger.addHandler(handler)
    return logger

# Example usage
if __name__ == '__main__':
    logger = setup_logger()
    logger.info('Logger is set up successfully.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    for i in range(100):
        logger.debug(f'Debugging message {i}')
