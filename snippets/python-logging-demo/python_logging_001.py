import logging
import sys

logger = logging.getLogger('Logger.example')
# the level should be the lowest level set in handlers
logger.setLevel(logging.DEBUG)
log_format = logging.Formatter('CRITICAL Failure - [%(levelno)d - %(levelname)s] %(asctime)s %(lineno)d - %(message)s')
critical_handler = logging.FileHandler('50 critical.txt')
critical_handler.setFormatter(log_format)
critical_handler.setLevel(logging.CRITICAL)
logger.addHandler(critical_handler)
log_format = logging.Formatter('ERROR    - [%(levelname)s] %(asctime)s %(lineno)d - %(message)s')
error_handler = logging.FileHandler('42 - error.txt')
error_handler.setFormatter(log_format)
error_handler.setLevel(logging.ERROR)
logger.addHandler(error_handler)
log_format = logging.Formatter('WARNING  - [%(levelname)s] %(asctime)s %(lineno)d - %(message)s')
warning_handler = logging.StreamHandler(sys.stderr)
warning_handler.setFormatter(log_format)
warning_handler.setLevel(logging.WARNING)
logger.addHandler(warning_handler)
log_format = logging.Formatter('INFO     - [%(levelname)s] %(asctime)s %(lineno)d - %(message)s')
info_handler = logging.StreamHandler(sys.stdout)
info_handler.setFormatter(log_format)
info_handler.setLevel(logging.INFO)
logger.addHandler(info_handler)
log_format = logging.Formatter('DEBUG     - [%(levelname)s] %(asctime)s %(lineno)d - %(message)s')
debug_handler = logging.FileHandler('00 - debug.txt')
debug_handler.setFormatter(log_format)
debug_handler.setLevel(logging.DEBUG)
logger.addHandler(debug_handler)
logger.debug('This is debug.')
logger.info('This is info.')
logger.warning('This is warning.')
logger.error('This is error.')
logger.critical('This is critical.')
logger.fatal('This is fatal.')
print('\n\n\n')
try:
    try:
        infini = 99 / 0
    except ZeroDivisionError as zde:
        logger.critical(zde)
        raise zde
except Exception as e:
    logger.error(e)
    logger.exception(e)
print(
    logging.CRITICAL,
    logging.FATAL,
    logging.ERROR,
    logging.WARNING,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG,
    logging.NOTSET,
)
