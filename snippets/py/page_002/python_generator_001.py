import logging
import time
from typing import Generator


def function[T: float](a: T, b: T, c: T) -> Generator[T, T, None]:
    i: T = 0  # type: ignore
    while a <= b:
        i = yield a
        a += c  # type: ignore
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
            print("\033[K", value, end="\r")
            i += 1
            j += 1
            if i % 8 == 0:
                # ! Example to 'send' Method
                b.send(-0.575)
            if value < -20:
                # ! Example to 'throw' Method
                b.throw(ValueError("Hello Google"))
            if value < -15:
                # ! Example to 'close' Method
                b.close()
        except StopIteration as se:
            logging.exception(se)
            break
        else:
            pass
        finally:
            pass
        time.sleep(0.25)

    print("End of Program")


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s")
    main()
    help(Generator)
    pass
