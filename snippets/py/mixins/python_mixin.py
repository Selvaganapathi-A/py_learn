from typing import Any


# Mixin Class
class DictionarySerializer:
    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


class Employee:
    def __init__(self, pay) -> None:
        self.pay = pay

    def __init_subclass__(cls) -> None:
        print(cls.__name__, 'was inherit me')

    def getPay(self):
        return self.pay


class Person(Employee, DictionarySerializer):
    first_name: str
    last_name: str

    def __init__(self, first_name: str, last_name: str, pay: int) -> None:
        super().__init__(pay)
        self.first_name = first_name
        self.last_name = last_name

    def __init_subclass__(cls) -> None:
        print(cls.__name__, 'was inherit me')

    def getPay(self) -> Any:
        return super().getPay() + 100


class Sub(Person):
    pass


class Super(Sub): ...


if __name__ == '__main__':
    ramya = Person('Ramya', 'P', 80)
    print(ramya.to_dict())
    print(ramya.getPay())
    meena = Person('Meena', 'R', 120)
    print(meena.to_dict())
    print(meena.getPay())
