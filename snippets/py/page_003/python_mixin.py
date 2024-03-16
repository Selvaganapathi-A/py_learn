from abc import (ABC, ABCMeta, abstractclassmethod, abstractmethod,
                 abstractproperty, abstractstaticmethod)
from typing import Any


# Mixin Class
class myMixin:

    def toDict(self):
        return self.__dict__


class Employee:

    def __init__(self, pay) -> None:
        self.pay = pay
        pass

    def __init_subclass__(cls) -> None:
        print(cls.__name__, "was inherit me")
        pass

    def getPay(self):
        return self.pay


class Person(myMixin, Employee):
    first_name: str
    last_name: str

    def __init__(self, first_name: str, last_name: str, pay: int) -> None:
        super(Person, self).__init__(pay)
        self.first_name = first_name
        self.last_name = last_name

    def getPay(self):
        return super(Person, self).getPay()


if __name__ == "__main__":
    ramya = Person("Ramya", "P", 80)
    print()
    print(ramya.toDict())
    print(ramya.getPay())

    meena = Person("Meena", "R", 120)
    print()
    print(meena.toDict())
    print(meena.getPay())

    pass
