from typing import Any


# using Metaclass
class SingletonMeta(type):
    _instances: dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]


class AppConfig(metaclass=SingletonMeta):
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
