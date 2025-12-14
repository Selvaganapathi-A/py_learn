from collections.abc import Callable
from typing import Any, TypeVar, cast

T = TypeVar('T')
Function = Callable[..., T]


def singleton(cls: Function) -> Function:
    instances: dict[Function, T] = {}  # type: ignore

    def get_instance(*args: Any, **kwargs: Any) -> T:  # type: ignore
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]  # type: ignore

    return cast(Function, get_instance)


@singleton
class AppConfig:
    def __init__(self, name: str) -> None:
        self.name = name

    def display(self):
        print(self.name)


def main():
    a = AppConfig('Fish')
    b = AppConfig('Cat')
    a.display()
    b.display()
    print(a is b)


if __name__ == '__main__':
    main()
