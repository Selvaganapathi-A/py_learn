from decimal import Decimal
from enum import IntEnum
from typing import Literal


class Storage(IntEnum):
    Bytes = 0
    KB = 1
    MB = 2
    GB = 3
    TB = 4
    PB = 5
    EB = 6
    ZB = 7
    YB = 8
    BB = 9


def binary_Storage(value: int = 1) -> int:
    return 1_024**value


def decimal_bytes(value: int = 1) -> int:
    return 1_000**value


def mapped_value() -> dict[int, str]:
    return {x.value: x.name for x in Storage}


def convert_to(
        value: int,
        to: Storage = Storage.PB,
        mapped: dict[int, str] = mapped_value(),
):
    i: int = 0
    tmp = Decimal(value)
    while True:
        i += 1
        tmp /= 1024
        if (900 > tmp) or (i >= 9) or (i >= to):
            break
    return f"{tmp:.2f} {mapped.get(i, 'BB')}"


def print_line(__char__: Literal[' ', '-', '*', '#'] = '-',
               *,
               length: int = 80):
    print(__char__ * length)


if __name__ == '__main__':
    print(convert_to(value=decimal_bytes(4) * Storage.GB, to=Storage.MB))
    print(convert_to(value=binary_Storage(4) * Storage.GB, to=Storage.MB))

    print(convert_to(value=decimal_bytes(4) * Storage.TB, to=Storage.GB))
    print(convert_to(value=binary_Storage(4) * Storage.TB, to=Storage.GB))

    print(convert_to(value=decimal_bytes(4) * 2, to=Storage.TB))
    print(convert_to(value=binary_Storage(4) * 2, to=Storage.TB))

    print(convert_to(value=decimal_bytes(5) * 2))
    print(convert_to(value=binary_Storage(5) * 2))
