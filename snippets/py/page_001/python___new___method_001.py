from typing import Any, Self, Type


class Connection:
    __spawned__instance__ = None

    def __new__(cls: Type[Self], *args: Any, **kwargs: Any) -> Self:
        if cls.__spawned__instance__ is None:
            print("Creating new Connection.")
            cls.__spawned__instance__ = super().__new__(cls)
        return cls.__spawned__instance__

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        print("Initializing Connection...")


if __name__ == "__main__":
    a = Connection(pangea=25)
    b = Connection(pangea=50)
    print(a)
    print(b)
    print(a == b)
