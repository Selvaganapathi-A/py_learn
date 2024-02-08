""" This is About Convert Any Number to Base of Any"""
from typing import List, Tuple


def number2base(number: int, base: int) -> Tuple[int]:
    """
    Convert Any number to Radix of Any

    example :
        number2base(8, 8) -> 10
    """
    if number < base:
        return (number,)
    mapped: List[int] = []
    temp: int
    while number >= base:
        temp = number % base
        mapped.append(temp)
        number = (number - temp) // base
    mapped.append(number)

    return tuple(mapped[::-1])


def main():
    """
    Main Method ...
    """
    number: int = 1_000_000_000_000
    radix: int = 247

    converted = number2base(number, radix)

    print(converted)


if __name__ == "__main__":
    main()
