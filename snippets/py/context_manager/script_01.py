import logging
import time
from collections.abc import Callable
from time import perf_counter_ns
from types import TracebackType
from typing import Any


class CustomContextManager:
    def __enter__(self):
        self.start = time.perf_counter()
        print('entering')
        return self

    def __exit__(
        self,
        exception: Exception,
        message: Any,
        traceback: TracebackType,
    ):
        end = time.perf_counter()
        print(end - self.start, 'microseconds in sync mode')
        # Exception Propagation if return False or
        # suppress particular exception with `isinstance` method
        return False


class MeasureTime:
    def __init__(self) -> None:
        self.start = perf_counter_ns()

    def __enter__(self) -> Callable[[], float]:
        """return `() => int`
        so that while exiting the time taken will be calculated and returned.
        """
        return lambda: perf_counter_ns() - self.start

    def __exit__(
        self,
        exception: Exception,
        message: Any,
        traceback: TracebackType,
    ) -> bool:
        """return
        * `True` if want to suppress errors.
        * `False` raises error until something captured."""
        if exception is ZeroDivisionError:
            print('exception       :', exception)
            print('message         :', message)
            print('error at line   :', traceback.tb_lineno)
            print('traceback       :', traceback)
            logging.exception(exception)
            return True
        return False


def main():
    with CustomContextManager():
        for _ in range(5):
            print('->', _)
            time.sleep(0.1)
    #
    print('-' * 80)
    with MeasureTime() as timer:
        time.sleep(2)
        time_taken = timer()
        print(f'{time_taken:n} ns')
        raise ZeroDivisionError('Unable to divide by zero.', 1, 0)


if __name__ == '__main__':
    import locale

    locale.setlocale(locale.LC_ALL, 'en_AU')
    main()
