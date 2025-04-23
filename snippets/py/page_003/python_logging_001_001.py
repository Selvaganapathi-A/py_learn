import logging


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S %p',
        filename='basic.log',
    )
    logging.debug('This is a DEBUG')
    logging.info('This is a INFO')
    logging.warning('This is a WARNING')
    logging.error('This is a ERROR')
    logging.critical('This is a Critical')


if __name__ == '__main__':
    main()
