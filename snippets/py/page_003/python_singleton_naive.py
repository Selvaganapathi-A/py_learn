from typing import Any


class Singleton(object):
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class NaiveSingleton(type):
    __naive_instances__: dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any):
        if cls not in cls.__naive_instances__:
            cls.__naive_instances__[cls] = super().__call__(*args, **kwargs)
        return cls.__naive_instances__[cls]


class Food(metaclass=NaiveSingleton):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs


if __name__ == "__main__":
    idli: Food = Food("idli", "hospital food.")
    burger: Food = Food("burger", "mc donalds.")
    print(idli.args)
    print(burger.args)
