import os,logging

os.makedirs('logs',exist_ok=True)

logger = logging.getLogger('ml_api_logger')
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s %(message)s'
)


file_handler = logging.FileHandler('logs/app.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.propagate = False
