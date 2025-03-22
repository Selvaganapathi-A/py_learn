"""
    Why Use __init_subclass__?
    *) To enforce rules or constraints on subclasses.
    *) To initialize class-level attributes in subclasses.
    *) To perform automatic registrations for subclass tracking.
    This is useful when designing frameworks, enforcing naming conventions,
or implementing class-level behaviors.
"""

import typing


class Animal:
    kind: str

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        print(args)
        print(kwargs)

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "kind"):
            raise AttributeError('"kind" is not present in sub class.')
        print(cls.__name__)
        print(hasattr(cls.__annotations__, "legs"))
        setattr(cls, "legs", 0)


class Bird(Animal):
    # kind: str = "Fly"
    legs: int = 0
    # raise TypeError, if "kind" not defined.


"""
✔ Why use this?
Ensures that all subclasses define category, enforcing consistency.
"""


class Vehicle:
    registered_models: set[typing.Type[typing.Self]] = set()

    def __init_subclass__(cls, *args, **kwargs: typing.Any) -> None:
        super(cls).__init_subclass__(*args, **kwargs)
        cls.registered_models.add(cls)


class Lorry(Vehicle):
    pass


class Truck(Vehicle):
    pass


class Car(Vehicle):
    pass


class Bike(Vehicle):
    pass


class Ducatti(Bike):
    pass


class Yamaha(Bike):
    pass


class BMW(Bike):
    pass


"""
    🔹 Key Takeaways
    __init_subclass__ runs automatically when a class is subclassed.
    It allows customization of subclasses without modifying their __init__.
    Useful for enforcing constraints, subclass registration,
    and modifying class attributes.
"""


def main():
    duck = Bird()
    print(duck.kind)
    print(duck.legs)
    print(Vehicle.registered_models)


if __name__ == "__main__":
    main()
