import time
from typing import Any, Callable


class Decorate:

    def __init__(self, function: Callable) -> None:
        self.function = function

    def __call__(self, a, b) -> Any:
        start = time.perf_counter_ns()
        return_value = self.function(a, b)
        end = time.perf_counter_ns()
        print(end - start, 'nano seconds.')
        return return_value


@Decorate
def some_fuction(a: int, b: int) -> int:
    return (a * b) + a + b


@Decorate
def other_function(a: int, b: int) -> int:
    return a - b


def extra_function(a: int, b: int) -> int:
    return a + b


#
print()
print(some_fuction(9, 8))
#
print()
print(other_function(7, 6))
#
decorate = Decorate(extra_function)
print(decorate(5, 4))
