import os 
import logging
import logging.handlers

from configs import LOG_DIR, LOG_FILE

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)

    file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=10485760, backupCount=10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


