import decimal
from decimal import Decimal

from some_module import combine


def main():
    a = 1
    b = 2
    r = combine(a, b)
    print(f'{a!r}+{b!r}={r!r}')
    #
    a = '1'
    b = '2'
    r = combine(a, b)
    print(f'{a!r}+{b!r}={r!r}')
    #
    a = [1]
    b = [2, 3]
    r = combine(a, b)
    print(f'{a!r}+{b!r}={r!r}')
    #
    a = True
    b = False
    r = combine(a, b)
    print(f'{a!r}+{b!r}={r!r}')
    #
    a = Decimal('1.2')
    b = Decimal('2.3')
    r = combine(a, b).quantize(Decimal('1.000'), rounding=decimal.ROUND_05UP)
    print(f'{a!r}+{b!r}={r!r}')


if __name__ == '__main__':
    main()
