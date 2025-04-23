from typing import Any, Self, Union


class Connection:
    __slots__: tuple[str, ...] = ('__initialized__',)
    __spawned__instance__: Union[Self, None] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls.__spawned__instance__ is None:
            print('Creating new Connection.')
            cls.__spawned__instance__ = super().__new__(cls)
            cls.__spawned__instance__.__initialized__ = False
        return cls.__spawned__instance__

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if self.__initialized__:
            return
        self.__initialized__: bool = True
        print('Initializing Connection...')


if __name__ == '__main__':
    a = Connection(pangea=25)
    b = Connection(pangea=50)
    print(a)
    print(b)
    print(a == b)
