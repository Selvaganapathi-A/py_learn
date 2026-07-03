import logging
import sys

logging.basicConfig(format='{message}', style='{', level=10)

# Check if GIL is enabled
if hasattr(sys, '_is_gil_enabled'):
    if sys._is_gil_enabled():
        logging.info('GIL is ENABLED')
    else:
        logging.info('GIL is DISABLED (no-GIL build)')
else:
    logging.info('This Python version does not support GIL detection.')
