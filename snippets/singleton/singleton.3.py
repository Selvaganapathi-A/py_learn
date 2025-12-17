from typing import Any


# using Metaclass
class Singleton(type):
    _instance: 'Singleton | None' = None

    def __new__(cls, *args: Any, **kwds: Any) -> Any:
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls, cls.__name__, (), {})
        return cls._instance


class AppConfig(Singleton):
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
