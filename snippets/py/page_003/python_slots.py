from subprocess import run
from typing import Any, Self


class Fruit:
    __slots__ = ("origin", "color")

    def __new__(cls, origin: str) -> Self:
        # cls.origin = "india"
        setattr(
            cls,
            "__annotations__",
            {
                "origin": str,
            },
        )
        obj = object.__new__(cls)
        obj.origin = origin
        return obj

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # self.origin = origin
        self.color = "red"


if __name__ == "__main__":
    run(("cls",), shell=True)
    fruit = Fruit("\tIron")
    print(f"{fruit.origin.expandtabs(5)!r}")
    # print(dir(Fruit))
    # print(Fruit.__dict__)
