from typing import NoReturn, TypeVar

T = TypeVar('T', str, int, float)

"""
T - can be either
        str or float or int
    not mixed type
"""


def some_function(a: T, b: T) -> T:
    return a + b


def alwaysRaiseError() -> NoReturn:
    raise KeyboardInterrupt()


def main():
    print(some_function(8, 5))
    print(some_function(8.4, 5.9))
    print(some_function('m', 'o'))
    # type error
    print(some_function('m', 4))
    _: NoReturn = alwaysRaiseError()


if __name__ == '__main__':
    main()
