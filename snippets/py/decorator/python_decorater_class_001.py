import time
from collections.abc import Callable
from typing import Any


class decorator:
    def __init__(self, function: Callable) -> None:
        self.function = function

    def __call__(self, a, b) -> Any:
        start = time.perf_counter_ns()
        return_value = self.function(a, b)
        end = time.perf_counter_ns()
        print(end - start, 'nano seconds.')
        return return_value


@decorator
def some_fuction(a: int, b: int) -> int:
    return (a * b) + a + b


@decorator
def other_function(a: int, b: int) -> int:
    return a - b


def extra_function(a: int, b: int) -> int:
    return a + b


def main():
    print(some_fuction(9, 8))
    print(other_function(7, 6))
    decorate = decorator(extra_function)
    print(decorate(5, 4))


if __name__ == '__main__':
    main()
