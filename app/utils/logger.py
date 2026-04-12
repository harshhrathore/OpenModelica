import logging
import sys
from typing import Optional

LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s — %(message)s"
DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
LOGGER_NAME: str = "OMSimLauncher"


class AppLogger:
    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_instance(cls) -> logging.Logger:
        if cls._instance is None:
            cls._instance = cls._create_logger()
        return cls._instance

    @classmethod
    def _create_logger(cls) -> logging.Logger:
        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger
