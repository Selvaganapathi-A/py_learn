import asyncio
import logging
import time
from dataclasses import dataclass
from time import perf_counter_ns
from types import TracebackType

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


class CustomContextManager:
    def __enter__(self):
        self.start = time.perf_counter()
        print('entering')
        return self

    def __exit__(
        self,
        exc_type: BaseException,
        exc: type[BaseException],
        exc_tb: TracebackType,
    ):
        end = time.perf_counter()
        print(end - self.start, 'microseconds in sync mode')
        return isinstance(exc, ZeroDivisionError)

    def wait(self):
        time.sleep(2)


class AsyncCustomContextManager:
    async def __aenter__(self):
        print('async entering')
        self.start = time.perf_counter()
        return self

    async def __aexit__(
        self,
        exc_type: BaseException,
        exc: type[BaseException],
        exc_tb: TracebackType,
    ):
        end = time.perf_counter()
        print(end - self.start, 'microseconds in async mode.')
        return isinstance(exc, ZeroDivisionError)

    async def asyncwait(self):
        await asyncio.sleep(2)


async def a_main():
    with CustomContextManager() as _:
        print(_)
        for x in range(5):
            _.wait()
        print(81 / 0)
    async with AsyncCustomContextManager() as _:
        print(_)
        await asyncio.gather(*(_.asyncwait() for x in range(5)))
        print(361 / 0)


if __name__ == '__main__':
    asyncio.run(a_main())


@dataclass(slots=True)
class Person:
    def __enter__(self):
        print('enter ctx')
        return self

    def __exit__(
        self,
        exc_type: Exception,
        exc_value: str,
        traceback: TracebackType,
    ) -> None:
        print('exit ctx')

    def sayHi(self):
        print('Person said Hi...')
        return 'hi'


class MeasureTime:
    def __enter__(self):
        self.start = perf_counter_ns()
        self.end = 0.0
        return lambda: self.end - self.start

    def __exit__(
        self,
        exc_type: Exception,
        exc_value: str,
        traceback: TracebackType,
    ) -> None:
        if exc_type is ZeroDivisionError:
            print(exc_value)
            print(traceback.tb_lineno)
            logging.exception(exc_type)
            # sys.exit(400)


def main() -> None:
    with Person() as p:
        print('hi')
        print('hello')
        p.sayHi()
        print('harness')
    # -------------------------------------- #
    tim = 0
    with MeasureTime() as mt:
        tim = mt
        time.sleep(6)
    print(tim())


if __name__ == '__main__':
    main()
