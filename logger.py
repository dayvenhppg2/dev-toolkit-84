import logging
import logging.handlers
import os

LOG_DIRECTORY = 'logs'
LOG_FILE = 'app.log'
MAX_BYTES = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5

if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

logger = logging.getLogger('crypto_toolkit')
logger.setLevel(logging.DEBUG)

file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(LOG_DIRECTORY, LOG_FILE),
    maxBytes=MAX_BYTES,
    backupCount=BACKUP_COUNT
)  
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)
