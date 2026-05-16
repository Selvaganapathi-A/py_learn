from typing import Self


class NoData:
    owner: type
    name: str
    value: str

    def __init__(self) -> None:
        self.value = 'from descriptor.'

    def __set_name__(self, owner: type, name: str) -> None:
        self.owner = owner
        self.name = name

    def __get__(self, instance: object | None, owner: type) -> Self | str:
        if instance is None:
            return self
        return 'from descriptor.'


class Thing:
    x: NoData = NoData()


def main() -> None:
    """
    Without __set__ method on descriptor, it can be overridden in other ways,
    rendering them useless.
    """

    t = Thing()
    print(t.x)

    t.__dict__['x'] = 'from instance dict.'  # shadowed by instance dict

    print(t.x)


if __name__ == '__main__':
    main()
