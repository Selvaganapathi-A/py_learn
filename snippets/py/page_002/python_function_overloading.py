from functools import singledispatch


@singledispatch
def func(arg):
    print(arg, "default")
    return 8


@func.register
def _(arg: int):
    print(arg, "int")
    return arg


@func.register  # type: ignore
def _(arg: str):
    print(arg, "float")
    return arg


@func.register  # type: ignore
def _(arg: list):
    print(arg, "list")
    return arg


@func.register  # type: ignore
def _(arg: tuple):
    print(arg, "tuple")
    return arg


def main():
    func(2)
    func(2.3)
    func("4.7")
    func("4.7".split("."))
    func((1, 2, 4, 5))


if __name__ == "__main__":
    main()
