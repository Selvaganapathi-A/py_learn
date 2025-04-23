from functools import partial
from typing import Self


class Infix(object):

    def __init__(self, func):
        self.func = func

    def __add__(self, __value: Self):
        ...

    def __or__(self, other):
        print(('__or__', self.func, other))
        return self.func(other)

    def __ror__(self, other):
        print(('__ror__', self.func, other))
        return Infix(partial(self.func, other))

    def __call__(self, v1, v2):
        return self.func(v1, v2)


@Infix
def addopt(x, y):
    return (x > y) - (x < y)


@Infix
def adder(x, y):
    print(x, y)
    return x + y


def main():
    x = 5
    y = 6
    z = 7
    print(x | addopt | y)
    print()
    print()
    print()
    print(x | adder | y | adder | z)
    print((7 * 12 / 240) * 60)
    print(dir(object))


if __name__ == '__main__':
    main()
