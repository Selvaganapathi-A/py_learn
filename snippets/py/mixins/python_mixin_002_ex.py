from dataclasses import dataclass

import json5


@dataclass
class Animal:
    name: str

    def serialize(self) -> dict[str, str]:
        return {'name': self.name, 'spicies': 'animal'}


@dataclass
class Monkey:
    def serialize(self) -> dict[str, str]:
        return {}


@dataclass
class Human(Animal, Monkey):
    name: str


if __name__ == '__main__':
    a = Human('ponnusami')
    print(a)
    print((json5.dumps(a.serialize(), indent=4), 1))
