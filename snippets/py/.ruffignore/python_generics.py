from dataclasses import dataclass, field


@dataclass
class Vehicle:
    name: str


@dataclass
class Car(Vehicle): ...


@dataclass
class Mini(Car): ...


@dataclass
class Boat(Vehicle): ...


@dataclass
class Plane(Vehicle): ...


@dataclass
class VehicleRegistry[T: Vehicle]:
    __vehicles__: list[T] = field(default_factory=list)

    def add(self, vehicle: T):
        self.__vehicles__.append(vehicle)

    def display(self):
        for index, vehicle in enumerate(self.__vehicles__, start=1):
            print(index, vehicle.name)


@dataclass
class LicensedVehicleRegistry[T: (Car, Plane)]:
    __items__: list[T] = field(default_factory=list)

    def add(self, item: T):
        self.__items__.append(item)

    def display(self):
        for index, vehicle in enumerate(self.__items__, start=1):
            print(index, vehicle.name)


def main():
    # Create Car Regitry
    carRegistry = VehicleRegistry[Car]()
    # Create Cars
    bmw = Car('bmw')
    audi = Car('audi')
    vw = Car('volkswagon')
    citroen = Car('citroen')
    toyoto = Mini('toyoto')
    # Add Cars to Car Registry
    carRegistry.add(bmw)
    carRegistry.add(audi)
    carRegistry.add(vw)
    carRegistry.add(citroen)
    carRegistry.add(toyoto)
    # Display Cars
    carRegistry.display()
    # ! ------------------------------------------------------------------------ ! #
    # Create Boat Registry
    boatRegistry = VehicleRegistry[Boat]()
    # Create Boats
    green_hunk = Boat('green_hunk')
    # Add Boats
    boatRegistry.add(green_hunk)
    # Display Boats
    boatRegistry.display()
    # ! ------------------------------------------------------------------------ ! #
    lv = LicensedVehicleRegistry[Car]()
    f13 = Plane('Fighter plane')
    lv.add(bmw)
    #
    # ! raises ArgumentError in pylance
    lv.add(f13)
    #
    # ! raises ArgumentError in pylance
    lv.add(green_hunk)
    #
    lv.display()


if __name__ == '__main__':
    main()
