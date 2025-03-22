import os
from dataclasses import dataclass
from typing import Any


@dataclass
class RedPrint:
    a: int = 5


def process(arg: Any):
    match arg:
        case dict():
            print(f"{arg} is Dictionary")
        case list():
            print(f"{arg} is List")
        case tuple():
            print(f"{arg} is tuple")
        case bool():
            print(f"{arg} is Boolean")
        case int():
            print(f"{arg} is Number")
        case float():
            print(f"{arg} is Number")
        case str():
            print(f"{arg} is String")
        case RedPrint():
            print("is object")
        case _:
            print("is Unknown to me")
    return


def main():
    process({"a": 2})
    process([9, 8])
    process((0, 8))
    process(2)
    process(9.8)
    process("venom")
    process(False)
    process(True)
    a = RedPrint(29)
    process(a)
    process(sum)
    print()


if __name__ == "__main__":
    os.system("cls")
    main()
