from typing import Self


class RangeOfValues:
    start: int
    stop: int
    _curr: int

    def __init__(self, start: int, stop: int) -> None:
        self.start = start
        self.stop = stop

    def __iter__(self) -> Self:
        self._curr = self.start
        return self

    def __next__(self) -> int:
        if self._curr >= self.stop:
            raise StopIteration
        self._curr += 1
        return self._curr


if __name__ == '__main__':
    for x in RangeOfValues(0, 25):
        print(x)
