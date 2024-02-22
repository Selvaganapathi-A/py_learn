from typing import Any, Type


def singleton(cls: Type[Any]):
    instance = None

    def wrapper(*args: Any, **kwargs: Any):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper


@singleton
class Plant:

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass


if __name__ == "__main__":
    a = Plant("audi", 98765)
    print(a)
    print()
    #
    b = Plant("bmw", 12345)
    print(b)
    print()
    #
    print(a, b)
    print(id(a), id(b))
    print(a == b)
    print(id(a) == id(b))
    pass
