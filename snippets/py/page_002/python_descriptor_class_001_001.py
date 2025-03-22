import logging
from typing import Self

from colorama import Fore

logging.basicConfig(
    format=Fore.MAGENTA + "%(asctime)s\n%(message)s" + Fore.RESET,
    level=logging.DEBUG,
)


class DescriptorClass[T, U]:
    def __set_name__(self, __cls: type[T], __variable: str) -> None:
        self.__cls: type[T] = __cls
        self.__var: str = __variable
        # ! For Storing And Retriving Values
        self.__object_store: dict[type[T], dict[T, dict[str, U]]] = {__cls: {}}
        # * For House keeping Purposes
        self.__object_registry: dict[type[T], dict[T, dict[str, int]]] = {__cls: {}}
        logging.debug(f"create Descriptor {__cls.__name__}.{__variable}")

    def __set__(self, __instance: T, __value: U) -> None:
        if __instance not in self.__object_registry[self.__cls]:
            self.__object_registry[self.__cls][__instance] = {}
        if "defined" not in self.__object_registry[self.__cls][__instance]:
            logging.debug(
                (f"Defining {self.__var} {self.__cls} {__instance} {__value}")
            )
            self.__object_registry[self.__cls][__instance]["defined"] = 1
        else:
            logging.debug(
                (
                    f"Modifying {self.__var} {self.__cls} {__instance} from "
                    f"{self.__object_store[self.__cls][__instance][self.__var]} "
                    f"to {__value}."
                )
            )
            self.__object_registry[self.__cls][__instance]["defined"] += 1
        if self.__cls not in self.__object_store:
            self.__object_store[self.__cls] = {}
        if __instance not in self.__object_store[self.__cls]:
            self.__object_store[self.__cls][__instance] = {}
        self.__object_store[self.__cls][__instance][self.__var] = __value

    def __get__(self, __instance: T, __cls: type[T]) -> U:
        if "accessed" in self.__object_registry[__cls][__instance]:
            self.__object_registry[__cls][__instance]["accessed"] += 1
        else:
            self.__object_registry[__cls][__instance]["accessed"] = 1
        logging.debug(
            (
                f"Accessing {__cls.__name__}.{self.__var} of {__instance} "
                f"'[{self.__object_registry[__cls][__instance]['accessed']}"
                " times.]'"
            )
        )
        if __instance not in self.__object_store[self.__cls]:
            raise ValueError("Value not set yet.")
        return self.__object_store[self.__cls][__instance][self.__var]


class City:
    area = DescriptorClass[Self, int]()

    def __init__(self, area: int) -> None:
        self.area = area


class State:
    total_area = DescriptorClass[Self, float]()

    def __init__(self, elevation: float) -> None:
        self.total_area = elevation


def main():
    p = City(200)
    p.area = 300
    print(p.area)
    print(p.area)
    print(p.area)
    print(p.area)
    print(p.area)
    q = State(410.01)
    r = State(420.01)
    s = State(430.01)
    t = State(440.01)
    u = State(450.01)
    q.total_area *= 1.1
    q.total_area *= 1.1
    q.total_area *= 1.1
    q.total_area *= 1.1
    q.total_area *= 1.1
    r.total_area *= 1.1
    r.total_area *= 1.1
    r.total_area *= 1.1
    r.total_area *= 1.1
    s.total_area *= 1.1
    s.total_area *= 1.1
    s.total_area *= 1.1
    t.total_area *= 1.1
    t.total_area *= 1.1
    u.total_area *= 1.1
    print(q.total_area)
    print(r.total_area)
    print(s.total_area)
    print(t.total_area)
    print(u.total_area)


if __name__ == "__main__":
    main()
