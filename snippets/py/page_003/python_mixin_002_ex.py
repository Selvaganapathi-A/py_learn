import collections
from collections import abc
from os import name
from typing import Any, AnyStr, List, TypedDict, TypeGuard

import json5
from dataclasses import dataclass


@dataclass
class Animal:
    name: str

    def serialize(self):
        return {"name": self.name, "spicies": "animal"}

    def sayWho(self):
        self.name


@dataclass
class Monkey:
    name: str

    def serialize(self):
        return {"name": self.name, "spicies": "monkey"}


@dataclass
class Human(Monkey, Animal):
    name: str


if __name__ == "__main__":
    a = Human("ponnusami")
    print(a)
    print(a.sayWho())
    print((json5.dumps(a.serialize()), 1))
    pass
