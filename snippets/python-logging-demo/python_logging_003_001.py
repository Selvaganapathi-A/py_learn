import logging
import os
from datetime import datetime
from enum import IntEnum, StrEnum
from logging.handlers import RotatingFileHandler


class Level(IntEnum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Field(StrEnum):
    ASCTIME = '%(asctime)s'
    CREATED = '%(created)f'
    FILENAME = '%(filename)s'
    FUNCTIONNAME = '%(funcName)s'
    LEVELNAME = '%(levelname)s'
    LEVELNO = '%(levelno)s'
    LINENO = '%(lineno)d'
    MESSAGE = '%(message)s'
    MODULE = '%(module)s'
    MSECS = '%(msecs)d'
    NAME = '%(name)s'
    PATHNAME = '%(pathname)s'
    PROCESS = '%(process)d'
    PROCESSNAME = '%(processName)s'
    RELATIVECREATED = '%(relativeCreated)d'
    THREAD = '%(thread)d'
    THREADNAME = '%(threadName)s'


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
