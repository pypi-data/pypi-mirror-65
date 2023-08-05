import logging
import sys
from loguru import logger as log


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        log_opt = log.opt(depth=7, exception=record.exc_info)
        log_opt.log(record.levelname, record.getMessage())


LOGGING_LEVEL = logging.DEBUG  # if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
log.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])


# if not DEBUG:
#     log.add("./log/debug_{time:%Y-%m-%d_%H-%M}.log", retention="2 days", level='DEBUG', backtrace=True, diagnose=True,
#             encoding='utf-8')
#     log.add("./log/info_{time:%Y-%m-%d_%H-%M}.log", retention="2 days", level='INFO', backtrace=True, diagnose=True,
#             encoding='utf-8')

def main():
    log.info('123')
