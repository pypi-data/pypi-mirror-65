import logging
import sys


def get_logger(logger_level=logging.INFO):
    formatter = logging.Formatter('%(message)s')

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logger_level)
    return logger


logger = get_logger()
