import logging
import sys


def get_logger(name: str, level: str = logging.WARNING):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    stderr_logger = logging.StreamHandler(sys.stderr)
    stderr_logger.setLevel(level)

    logger.addHandler(stderr_logger)

    return logger
