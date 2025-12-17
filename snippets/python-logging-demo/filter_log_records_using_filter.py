import importlib
import logging
import sys
# formatter: ModuleType = importlib.import_module(
#     'formatter', 'zypress.python-logging-demo.formatter'
# )
# test: ModuleType = importlib.import_module('test', 'zypress.python-logging-demo.test')
from enum import IntEnum
from types import ModuleType

from custom_formatter import BashFormatter
from custom_test import test_logger


class LogLevel(IntEnum):
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0


class CustomLogFilter(logging.Filter):
    def __init__(self, *loglevels: LogLevel, name: str = '') -> None:
        super().__init__(name)
        self.logLevels = set(loglevels)
        self.logLevelCount = len(loglevels)

    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        if self.logLevelCount > 0:
            return record.levelno in self.logLevels and super().filter(record)
        else:
            return super().filter(record)
        # if self.nlen == 0:
        #     return True
        # elif self.name == record.name:
        #     return True
        # elif record.name.find(self.name, 0, self.nlen) != 0:
        #     return False
        # return record.name[self.nlen] == '.'


def main():
    """
    filter records by
        logging.Filter
    """
    logger = logging.getLogger('demo.google.hub')

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(BashFormatter('{name} - {levelno: >2d} - {message}', style='{'))
    handler.addFilter(
        CustomLogFilter(
            LogLevel.INFO,
            LogLevel.DEBUG,
            LogLevel.CRITICAL,
            LogLevel.FATAL,
            LogLevel.ERROR,
            name='demo.google',
        )
    )
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    test_logger(logger)


if __name__ == '__main__':
    main()
