from functools import lru_cache

__all__: list[str] = [
    'fibbonocci_number',
]


@lru_cache(maxsize=32)
def fibbonocci_number(number: int):
    a: int = 0
    b: int = 1
    while a < number:
        a, b = b, a + b
    return a


def main():
    r = fibbonocci_number(1000)
    print(r)
    #
    r = fibbonocci_number(1000)
    print(r)
    pass


if __name__ == '__main__':
    main()
    pass
