import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevels(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    DEBUG = "DEBUG"



def configure_logging(level: LogLevels = LogLevels.INFO) -> None:
    log_levels = [level.value for level in LogLevels]

    if level not in log_levels:
        logging.basicConfig(level=LogLevels.ERROR)
        return

    if level == LogLevels.DEBUG:
        logging.basicConfig(level=level, format=LOG_FORMAT_DEBUG)
        return

    logging.basicConfig(level=level)
