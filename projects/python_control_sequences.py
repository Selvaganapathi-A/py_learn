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
    return f'{tmp:.2f} {mapped.get(i, "BB")}'


def as_computer_storage(value: int = 1) -> int:
    return 1_024**value


def as_vendor_storage(value: int = 1) -> int:
    return 1_000**value


def print_line(__char__: Literal[' ', '-', '*', '#'] = '-', *, length: int = 80):
    print(__char__ * length)


def Partition_by_Size(SSD_CAPACITY: int, units: Storage):
    PARTITION_SIZE: int = as_computer_storage(units - 1) * 310

    CAPACITY_DECIMAL: int = as_vendor_storage(units) * SSD_CAPACITY
    AS_MACHINE: int = as_computer_storage(units) * SSD_CAPACITY

    print(f'By Vendor         : {CAPACITY_DECIMAL:_}')
    print(f'By Machine        : {AS_MACHINE:_}')

    TOTAL_SYSTEM_PARTITION: int = CAPACITY_DECIMAL

    value: int = TOTAL_SYSTEM_PARTITION - 1024 * Storage.MB
    index: int = 1

    print_line('*')

    print(
        'Usable Space      :\n'
        f'{convert_to(AS_MACHINE, to=Storage.KB):>25} - '
        f'{convert_to(AS_MACHINE, to=Storage.MB):>25}\n'
        f'{convert_to(AS_MACHINE, to=Storage.GB):>25} - '
        f'{convert_to(AS_MACHINE, to=Storage.TB):>25}\n'
        f'{convert_to(AS_MACHINE, to=Storage.PB):>25} - '
        f'{convert_to(AS_MACHINE, to=Storage.EB):>25}'
    )

    print_line('*')

    print(
        'Partition Size    :\n'
        f'{convert_to(PARTITION_SIZE, to=Storage.KB):>20} - '
        f'{convert_to(PARTITION_SIZE, to=Storage.MB):>20} - '
        f'{convert_to(PARTITION_SIZE, to=Storage.GB):>20}'
    )

    print_line('-')

    while True:
        tmp: int = PARTITION_SIZE if 2 * PARTITION_SIZE < value else value

        print(
            f'{index:>3} {100 * tmp / TOTAL_SYSTEM_PARTITION:5.2f}% - '
            f'{convert_to(tmp, to=Storage.KB):>12} - '
            f'{convert_to(tmp, to=Storage.MB):>8} - '
            f'{convert_to(tmp, to=Storage.GB)}'
        )

        index += 1
        value -= PARTITION_SIZE

        if value < PARTITION_SIZE:
            break


def main(): ...


if __name__ == '__main__':
    print_line('#')
    main()
    print_line('#')
