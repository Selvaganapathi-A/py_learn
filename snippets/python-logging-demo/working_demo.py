import logging


def test_logger(logger: logging.Logger):
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    try:
        print(1 / 0)
    except ZeroDivisionError as e:
        logger.exception(e)
    logger.error('error message')
    logger.critical('critical message')
