import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def func_logger(hashString: str):
    logFile = os.sep.join(('.', '⌘ test ⌘', 'log', hashString + '.txt'))
    logger = logging.getLogger(hashString)
    logger.setLevel(logging.INFO)
    loggerFormat = logging.Formatter('%(message)s')
    loggerHandler = RotatingFileHandler(
        logFile,
        maxBytes=10 * 1024 * 1024,
        backupCount=20,
        mode='W',
        encoding='UTF-8',
    )
    loggerHandler.setLevel(logging.INFO)
    loggerHandler.setFormatter(loggerFormat)
    logger.addHandler(loggerHandler)
    logger.info('*' * 120)
    logger.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S - %f').center(120))
    logger.info('*' * 120)
    return logger


if __name__ == '__main__':
    pass
