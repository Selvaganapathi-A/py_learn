from typing import ClassVar, Self


class Vehicle:
    __final__: ClassVar[bool] = True

    def __init__(self, model: str) -> None:
        self.model: str = model

    def drive(self: Self):
        return self.model


class Car(Vehicle):
    def __init__(self, model: str) -> None:
        super().__init__(model)

    def drive(self: Self):
        return 'Car' + self.model


class Boat(Vehicle):
    def __init__(self, model: str) -> None:
        super().__init__(model)

    def sail(self: Self):
        return 'Boat' + self.model


class Registry[T: Vehicle]:
    def __init__(self) -> None:
        self.vehicles: list[T] = []

    def add_vehicle(self, vehicle: T):
        self.vehicles.append(vehicle)


def main():
    registry: Registry[Car] = Registry[Car]()
    honda = Car('Honda')
    registry.add_vehicle(Car('Honda'))
    registry.add_vehicle(Car('Tesla'))

    # ! raises type error
    # boat cannot added to vehicle registry
    registry.add_vehicle(Boat('Toyoto'))

    # ! Class Variable should'nt be assigned through class instance.
    honda.__final__ = False
    #
    print(honda.__final__)
    print(getattr(Vehicle, '__final__'))
    print(getattr(Car, '__final__'))  # returns True
    print(honda.__final__)


if __name__ == '__main__':
    main()
