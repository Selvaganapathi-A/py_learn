from typing import Any, Type


def singleton(cls: type[Any]):
    instance = None

    def wrapper(*args: Any, **kwargs: Any):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper


@singleton
class Plant:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...


if __name__ == '__main__':
    a = Plant('audi', 98765)
    print(a)
    b = Plant('bmw', 12345)
    print(b)
    print(a, b)
    print(id(a), id(b))
    print(a == b)
    print(id(a) == id(b))
