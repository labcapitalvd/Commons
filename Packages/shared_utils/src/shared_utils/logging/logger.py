# shared_utils/logging.py

import os
import logging
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

_LOG_LEVELS: dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def _get_log_level() -> int:
    return _LOG_LEVELS.get(
        os.environ.get("LOGLEVEL", "INFO").upper(),
        logging.INFO,
    )


def configure_logging() -> None:
    logging.basicConfig(
        level=_get_log_level(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    return get_logger(name)
