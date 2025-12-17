from collections.abc import Sequence
from functools import lru_cache

__all__: Sequence[str] = ('fibbonocci_number',)


@lru_cache(maxsize=32)
def fibbonocci_number(number: int):
    a: int = 0
    b: int = 1
    while a < number:
        a, b = b, a + b
        # temp = a
        # a = b
        # b = a + temp
        # print('\t', a, b)
    return a


def fibbonocci_sequence(number: int):
    a: int = 0
    b: int = 1
    # yield a
    # yield b
    while True:
        a, b = b, a + b
        if a > number:
            break
        yield a
    return a


def main():
    n = 2000
    r = fibbonocci_number(n)
    print(n, r)
    n = 19
    r = fibbonocci_number(n)
    print(n, r)
    for x in fibbonocci_sequence(20):
        print('&&&', x)


if __name__ == '__main__':
    main()
