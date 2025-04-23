import collections
from collections import abc
from dataclasses import dataclass
from os import name
from typing import Any, AnyStr, List, TypedDict, TypeGuard

import json5


@dataclass
class Animal:
    name: str

    def serialize(self):
        return {'name': self.name, 'spicies': 'animal'}
        self.name


@dataclass
class Monkey:

    def serialize(self):
        retur


@dataclass
class Human(Monkey, Animal):
    name: str


if __name__ == '__main__':
    a = Human('ponnusami')
    print(a)
    print(a.sayWho())
    print((json5.dumps(a.serialize(), indent=4), 1))
