from typing import Any, Self, TypeVar


class A:
    @staticmethod
    def __new__(cls: type["A"], value: str) -> type["A"]:
        print("__new__ method.")
        print(dir(object))
        # print(help(type))
        return object.__new__(cls)

    def __init__(self, value: str) -> None:
        print("__init__ method.")
        self.value = value
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"

    def __call__(self, value: str) -> Any:
        print("__call__ method.")
        self.value = value
        return self


if __name__ == "__main__":
    print()
    a = A("poll")

    print(a)
    b = a("poland")

    print(b)
    print(a, b)
    print(b == a, id(b), id(a))

    pass
