import logging
import os

if not os.path.exists('logs'):
        os.makedirs('logs')

logging.basicConfig(level=logging.INFO, format=(
        "%(asctime)s | "
        "%(filename)s:%(lineno)d | "
        "%(levelname)s | "
        "%(message)s"),
        handlers=[logging.FileHandler('logs/server.log', encoding='utf-8'), logging.StreamHandler()])

logger = logging.getLogger("crazy_taxi")