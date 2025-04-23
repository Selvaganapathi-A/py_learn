from functools import lru_cache


@lru_cache(20)
def fibbonocci(n: int):
    current: int
    prev1: int = 0
    prev2: int = 1
    for _ in range(2, n):
        current = prev1 + prev2
        prev1 = prev2
        prev2 = current
        print('\t\t', prev2)
    return current


def main():
    print(fibbonocci(24))
    print(fibbonocci(12))
    print(fibbonocci(24))
    print(fibbonocci(13))
    print(fibbonocci(14))
    print(fibbonocci(12))
    pass


if __name__ == '__main__':
    main()
    pass
