from abc import ABCMeta


class Fruit(type):
    handlers: dict = {}

    def __new__(metaclass_, name, bases, attrs, **optional_dict):
        # cls_ = super().__new__(metaclass_, name, bases, attrs)
        cls_ = type(name, bases, attrs)
        if cls_.__name__ not in metaclass_.handlers:
            metaclass_.handlers[cls_.__name__] = cls_
        else:
            raise ValueError(cls_.__name__, "Created Already.")
        for k, v in optional_dict.items():
            setattr(cls_, k, v)
        return cls_


class Apple(metaclass=Fruit, origin="india", color="red"):
    origin: str
    color: str

    def __init__(self, origin: str, color: str) -> None:
        self.origin = origin
        self.color = color


class Orange(metaclass=Fruit):
    pass


class Banana(metaclass=Fruit):
    pass


class Guaua(metaclass=Fruit):
    pass


class PineApple(metaclass=Fruit):
    pass


class StrawBerry(metaclass=Fruit):
    pass


class BlueBerry(metaclass=Fruit):
    def __new__(cls):
        print("Hi")
        return object.__new__(cls)
        pass

    pass


if __name__ == "__main__":
    from subprocess import call, check_output, run

    run(
        ("cls",),
        shell=True,
    )

    a = Apple("iran", "black")

    print(a.origin)
    print(a.color)
    print()
    print(Apple.origin)
    print(Apple.color)
    print()
    print(type(a))
    print(type(Apple))
    print()
    print(Fruit.handlers)

    print("-" * 80)
    bb = BlueBerry()
    print(bb)
    print(type(bb))
    print("-" * 80)
