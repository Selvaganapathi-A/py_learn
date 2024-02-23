from decimal import Decimal
from typing import Callable, TypeAlias

from typing_extensions import TypeVar

# * Generic bound to int, float, str, Decimal
T = TypeVar("T", int, float, str, Decimal)

A: TypeAlias = tuple[int, int]
function: TypeAlias = Callable[[int, int, int], int]


def lambda_add(a: T, b: T) -> T:
    return a + b


def main():
    xd: A = (9, 8)
    print(xd)
    pass


if __name__ == "__main__":
    # help(TypeAlias)
    main()

    pass
