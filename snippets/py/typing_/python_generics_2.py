import typing
from collections.abc import Callable
from typing import NewType, TypeAlias, TypeVar

Q = NewType('Q', int)
T = TypeVar('T', str, bytes, bytearray)
type m = typing.Annotated[m, str, bytes]
function: TypeAlias = Callable[[int, str], int]


def func(a: function, b: int, c: str, d: Q = Q(45)):
    print(a(b, c), d)
    return b


def main():
    def some_function(x, y):
        return x + len(y)

    func(some_function, 45, 'bing')
    func(some_function, 93, 'google')
    func(
        some_function,
        93,
        "we die with the dying. We're Born with the dead.",
    )


if __name__ == '__main__':
    main()
    # #
    # help(TypeGuard)
    # help(TypeAlias)
    help(typing)
