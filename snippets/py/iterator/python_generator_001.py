import logging
import time
from collections.abc import Generator


def function[T: float](a: T, b: T, c: T) -> Generator[T, T, None]:
    i: T = 0  # type: ignore
    while a <= b:
        a += c  # type: ignore
        i = yield a
        if isinstance(i, float):
            # print(i, "inside function")
            c = i


def main():
    i: int = 0
    j: int = 0
    b = function(0.0, 20.0, 0.1)
    while True:
        try:
            value = next(b)
            print('\033[K', value, end='\r')
            i += 1
            j += 1
            if value > 8:
                # ! Example to 'send' Method
                b.send(-2)
            if value < -20:
                # ! Example to 'throw' Method
                b.throw(ValueError('Hello Google'))
            if value < -45:
                # ! Example to 'close' Method
                b.close()
        except StopIteration as se:
            logging.exception(se)
            break
        time.sleep(0.25)
    print('End of Program')


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s')
    main()
    # help(Generator)
