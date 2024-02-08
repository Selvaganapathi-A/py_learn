from dataclasses import dataclass
from time import perf_counter_ns
from types import TracebackType

import logging
import time


"""
With context managers, you can perform any pair of operations that needs to be done
before and after another operation or procedure, such as:

Open and close
Lock and release
Change and reset
Create and delete
Enter and exit
Start and stop
Setup and teardown
"""


@dataclass(slots=True)
class Person:
    def __enter__(self):
        print("enter ctx")
        return self

    def __exit__(
        self, exc_type: Exception, exc_value: str, traceback: TracebackType
    ) -> None:
        print("exit ctx")

    def sayHi(self):
        print("Person said Hi...")
        return "hi"


class MeasureTime:
    def __enter__(self):
        self.start = perf_counter_ns()
        self.end = 0.0
        return lambda: self.end - self.start

    def __exit__(
        self, exc_type: Exception, exc_value: str, traceback: TracebackType
    ) -> None:
        if exc_type is ZeroDivisionError:
            print(exc_value)
            print(traceback.tb_lineno)
            logging.exception(exc_type)
            # sys.exit(400)


def main() -> None:
    with Person() as p:
        print("hi")
        print("hello")
        p.sayHi()
        print("harness")
    # -------------------------------------- #
    tim = 0

    with MeasureTime() as mt:
        tim = mt
        time.sleep(6)
    print(tim())
    pass


if __name__ == "__main__":
    main()
