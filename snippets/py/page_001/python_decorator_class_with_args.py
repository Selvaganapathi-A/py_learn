import time
from typing import Any, Callable


class Decorate:
    def __init__(self, arg: int) -> None:
        self.arg = arg

    def __call__(self, function: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(a: int, b: int) -> int:
            start = time.perf_counter_ns()
            return_value: Any = function(a, b) * self.arg
            end = time.perf_counter_ns()
            print(end - start, "nano seconds.")
            return return_value

        return wrapper


@Decorate(arg=2)
def some_func(a: int, b: int) -> int:
    return (a * b) + a + b


@Decorate(arg=4)
def other_func(a: int, b: int) -> int:
    return a - b


def some_other_func(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    print()
    print(some_func(9, 8))
    print()
    print(other_func(7, 6))
    print()
    decorate = Decorate(3)
    print(decorate(some_other_func)(5, 4))
