import logging
import sys


def main():
    spiderman = logging.getLogger('spiderman')
    spiderman.setLevel(logging.ERROR)
    spiderman.addHandler(logging.StreamHandler(sys.stderr))
    spiderman.addHandler(logging.FileHandler('rt.log', 'a'))
    venom = logging.getLogger('venom')
    venom.setLevel(logging.WARNING)
    venom.addHandler(logging.StreamHandler(sys.stdout))
    spiderman.info('This is info for Spiderman')
    spiderman.error('This is Error for Spiderman')
    spiderman.critical('This is Critical for Spiderman')
    venom.info('This is info for N')
    venom.warning('This is warning for N')
    venom.error('This is error for N')
    venom.critical('This is critical for N')


if __name__ == '__main__':
    main()
