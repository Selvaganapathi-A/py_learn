import importlib
import logging
import sys
from types import ModuleType

from custom_formatter import BashFormatter
from custom_test import test_logger


# formatter: ModuleType = importlib.import_module(
#     'formatter', 'zypress.python-logging-demo.formatter'
# )
# test: ModuleType = importlib.import_module('test', 'zypress.python-logging-demo.test')


class DebugFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == logging.DEBUG


def main():
    """
    filter records by
        logging.Filter
    """
    logger = logging.getLogger('demo')
    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(DebugFilter('demo-filter'))
    handler.setFormatter(BashFormatter('{message}', style='{'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    test_logger(logger)


if __name__ == '__main__':
    main()
