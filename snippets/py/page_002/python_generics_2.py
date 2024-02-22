from typing import Callable, LiteralString, NewType, Text, Type, TypeAlias
from typing import TypeGuard, TypeVar


import typing

Q = NewType("Q", int)

T = TypeVar("T", str, bytes, bytearray)

type m = typing.Annotated[m, str, bytes]


alpha: TypeAlias = Callable[[int, str], int]


def func(a: alpha, b: int, c: str):
    print(a(b, c))
    return b


def main():
    some_function: alpha = lambda x, y: x + len(y)

    func(some_function, 45, "bing")
    func(some_function, 93, "google")
    func(
        some_function,
        93,
        "we die with the dying. We're Born with the dead.",
    )

    pass


if __name__ == "__main__":
    # main()

    # #
    # help(TypeGuard)
    # help(TypeAlias)
    help(typing)

    pass

    pass

    pass
