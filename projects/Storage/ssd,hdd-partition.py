from decimal import Decimal
from enum import IntEnum, StrEnum
from functools import lru_cache
from typing import Literal


class Storage(StrEnum):
    Byte = 'byte'  # Byte
    Kilobyte = 'Kilo byte'  # Kilobyte
    Megabyte = 'Mega byte'  # Megabyte
    Gigabyte = 'Giga byte'  # Gigabyte
    Terabyte = 'Tera byte'  # Terabyte
    Petabyte = 'Peta byte'  # Petabyte
    Exabyte = 'Exa byte'  # Exabyte
    Zettabyte = 'Zetta byte'  # Zettabyte
    Yottabyte = 'Yotta byte'  # Yottabyte
    Brontobyte = 'Bronto byte'  # Brontobyte
    Geopbyte = 'Geop byte'  # Geopbyte
    Saganbyte = 'Sagan byte'  # Saganbyte
    Pijabyte = 'Pija byte'  # Pijabyte
    Alphabyte = 'Alpha byte'  # Alphabyte
    Kryatbyte = 'Kryat byte'  # Kryatbyte
    Amosbyte = 'Amos byte'  # Amosbyte
    Pectrolbyte = 'Pectrol byte'  # Pectrolbyte
    Bolgerbyte = 'Bolger byte'  # Bolgerbyte
    Sambobyte = 'Sambo byte'  # Sambobyte
    Quesabyte = 'Quesa byte'  # Quesabyte
    Kinsabyte = 'Kinsa byte'  # Kinsabyte
    Rutherbyte = 'Ruther byte'  # Rutherbyte
    Dubnibyte = 'Dubni byte'  # Dubnibyte
    Seaborgbyte = 'Seaborg byte'  # Seaborgbyte
    Bohrbyte = 'Bohr byte'  # Bohrbyte
    Hassiubyte = 'Hassiu byte'  # Hassiubyte
    Meitnerbyte = 'Meitner byte'  # Meitnerbyte
    Darmstadbyte = 'Darmstad byte'  # Darmstadbyte
    Roentbyte = 'Roent byte'  # Roentbyte
    Coperbyte = 'Coper byte'  # Coperbyte


class MemoryUnit(IntEnum):
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


class StorageMedium:
    def __init__(self, capacity: int, unit: MemoryUnit) -> None:
        self.total_capacity = capacity * (1000**unit)
        self._partitions: list[int] = []

    def partition(
        self,
        capacity: int,
        unit: MemoryUnit,
        target_system: Literal['windows', 'linux'],
    ) -> None:
        partition_size = capacity
        if target_system == 'linux':
            partition_size = partition_size * 1000**unit
        else:
            partition_size = partition_size * 1024**unit
        available_storage = self.total_capacity
        while (2 * partition_size) <= available_storage:
            self._partitions.append(partition_size)
            available_storage -= partition_size
        if 0 < available_storage:
            self._partitions.append(available_storage)


@lru_cache(1000, True)
def convert_to(
    value: int,
    to: MemoryUnit = MemoryUnit.TB,
    target_system: Literal['windows', 'linux'] = 'windows',
):
    print('===>', value)
    divisor: int
    if target_system == 'windows':
        divisor = 1024
    else:
        divisor = 1000
    i: int = 0
    tmp = Decimal(value)
    while True:
        i += 1
        tmp /= divisor
        if (900 > tmp) or (i >= to):
            break
    return tmp


def main():
    # Partition_by_Size(2000, StorageUnit.GB)
    ssd_1tb = StorageMedium(2, MemoryUnit.TB)
    ssd_1tb.partition(256, MemoryUnit.GB, 'windows')
    for i, partition in enumerate(ssd_1tb._partitions, start=1):
        print(
            i,
            convert_to(
                partition,
                MemoryUnit.GB,
                'windows',
            ),
            'GB',
        )


if __name__ == '__main__':
    main()
