import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

log_file = Path("app.log")
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)

console_format = logging.Formatter('%(levelname)-8s %(message)s')
console_handler.setFormatter(console_format)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.propagate = False
