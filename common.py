import logging
from config.config_loader import config


def setup_logging():
    logger = logging.getLogger()

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s : %(message)s")
    stream_handler.setFormatter(formatter)

    logger.setLevel(level=config.log_level)
    if not logger.handlers:
        logger.addHandler(stream_handler)
