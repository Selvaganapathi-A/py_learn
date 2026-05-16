from typing import Self


class Data:
    owner: type
    name: str
    value: str

    def __init__(self) -> None:
        self.value = 'from descriptor'

    def __set_name__(self, owner: type, name: str) -> None:
        self.owner = owner
        self.name = name

    def __get__(self, instance: object | None, owner: type) -> Self | str:
        if instance is None:
            return self
        return 'from descriptor.'

    def __set__(self, instance: object | None, value: str) -> None:
        instance.__dict__['data'] = value


class Thing:
    x: Data = Data()


def main() -> None:
    """
    Descriptor's set method precedes over instance's dict.
    """
    t = Thing()
    print(t.x)
    t.__dict__['x'] = 'from instance dict.'  # descriptor still wins. (data descriptor precedence)
    print(t.x)
    print(t.__dict__)


if __name__ == '__main__':
    main()
