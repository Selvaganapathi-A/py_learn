import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')


def shout_if_called(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        """
        Docstring for wrapper

        :param args: Description
        :type args: P.args
        :param kwargs: Description
        :type kwargs: P.kwargs
        :return: Description
        :rtype: R
        """
        print('[*]', func.__qualname__, 'is called with', *args, kwargs)
        return func(*args, **kwargs)

    return wrapper


@shout_if_called
def add(a: int, b: int, /) -> int:
    """
    Docstring for add

    :param a: Description
    :type a: int
    :param b: Description
    :type b: int
    :return: Description
    :rtype: int
    """
    return a + b


@shout_if_called
def expose(*, sts: str) -> str:
    """
    Docstring for xpo

    :param sts: Description
    :type sts: str
    """
    return sts * 10


def main():
    print(add(1, 6))
    print(expose(sts='*'))
    print(add.__doc__)


if __name__ == '__main__':
    main()
