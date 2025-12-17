from enum import StrEnum
from typing import Any


class Color(StrEnum):
    reset = '\x1b[0m'
    darkgray = '\x1b[38;5;0m'
    lightgray = '\x1b[38;5;8m'
    red = '\x1b[38;5;1m'
    green = '\x1b[38;5;2m'
    yellow = '\x1b[38;5;3m'
    blue = '\x1b[38;5;4m'
    violet = '\x1b[38;5;5m'
    gray = '\x1b[38;5;6m'
    cyan = '\x1b[38;5;51m'


class Display:
    def __init__(self, color: Color) -> None:
        self.__color__ = color

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print(self.__color__, end='')
        print(*args)
        print(Color.reset, end='')


def main():
    for x in range(256):
        print(f'\x1b[38;5;{x}m {x:0>3d}\x1b[0m', end=' ')
        if x % 16 == 15:
            print()
    for x in range(256):
        print(f'\x1b[48;5;{x}m {x:0>3d}\x1b[0m', end=' ')
        if x % 16 == 15:
            print()
    display = Display(Color.darkgray)
    display('Hello Google')


if __name__ == '__main__':
    main()
