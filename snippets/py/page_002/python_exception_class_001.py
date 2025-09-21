import logging


class UnsupportedStream(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


if __name__ == '__main__':
    try:
        raise UnsupportedStream('java code')
        raise (Exception('Pandora'))
    except UnsupportedStream as ue:
        logging.exception(ue)
    except Exception as e:
        logging.exception(e)
