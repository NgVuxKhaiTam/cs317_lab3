import logging
import os
from logging.handlers import SysLogHandler, RotatingFileHandler

LOG_PATH = os.getenv('LOG_PATH', 'logs/app.log')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Formatter chung
t_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# stdout handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(t_formatter)
logger.addHandler(console)

# syslog handler (server logs)
syslog = SysLogHandler(address='/dev/log')
syslog.setLevel(logging.WARNING)
syslog.setFormatter(t_formatter)
logger.addHandler(syslog)

# file handler (application log)
file_handler = RotatingFileHandler(LOG_PATH, maxBytes=10**7, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(t_formatter)
logger.addHandler(file_handler)