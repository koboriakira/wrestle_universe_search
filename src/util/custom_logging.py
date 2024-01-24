import logging
from logging import Logger
from typing import Optional
import os


def get_logger(name: Optional[str] = None) -> Logger:
    logger = logging.getLogger(name)

    if os.getenv("ENVIRONMENT") == "dev":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # handler1: 標準出力
    handler1 = logging.StreamHandler()
    handler1.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)8s %(message)s"))
    logger.addHandler(handler1)

    return logger
