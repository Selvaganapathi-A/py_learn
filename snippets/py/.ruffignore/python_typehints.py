from typing import Self


class Vehicle:
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
        self.vehicles: list[T] = list()

    def add_vehicle(self, vehicle: T):
        self.vehicles.append(vehicle)


def main():
    registry: Registry[Car] = Registry[Car]()
    registry.add_vehicle(Car('Honda'))
    registry.add_vehicle(Car('Tesla'))
    # registry.add_vehicle(Boat("Toyoto"))


if __name__ == '__main__':
    main()
