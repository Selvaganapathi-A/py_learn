from decimal import Decimal
from typing import Callable, TypeAlias

from typing_extensions import TypeVar

# * Generic bound to int, float, str, Decimal
T = TypeVar('T', int, float, str, Decimal)
A: TypeAlias = tuple[int, int]
function: TypeAlias = Callable[[int, int, int], float]


def lambda_add(a: T, b: T) -> T:
    return a + b


def green(x: int, y: int, z: int) -> float:
    return (x + y + z) / 3


def main():
    yellow: function = green
    print(yellow)
    print(yellow.__annotations__)
    print(yellow(7, 9, 8))
    xd: A = (9, 8)
    print(xd)


if __name__ == '__main__':
    # help(TypeAlias)
    main()
