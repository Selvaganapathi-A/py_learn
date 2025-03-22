import importlib
import logging
import sys
from types import ModuleType

from custom_formatter import BashFormatter
from custom_test import test_logger


# formatter = importlib.import_module('formatter',
#                                     'zypress.python-logging-demo.formatter')
# test = importlib.import_module('test', 'zypress.python-logging-demo.test')
class DebugHandler(logging.StreamHandler):
    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno == logging.DEBUG:
            return super().emit(record)
        return None


def main():
    """
    filter records by
        logging.Streamhandler
    """
    logger = logging.getLogger("demo")
    handler = DebugHandler(sys.stderr)
    handler.setFormatter(
        BashFormatter("| {levelname:>12s} | {message:<24s} |", style="{")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    test_logger(logger)


if __name__ == "__main__":
    main()
