from dataclasses import dataclass

import json5


@dataclass
class Animal:
    name: str

    def serialize(self):
        return {'name': self.name, 'spicies': 'animal'}


@dataclass
class Monkey:
    def serialize(self):
        return


@dataclass
class Human(Monkey, Animal):
    name: str


if __name__ == '__main__':
    a = Human('ponnusami')
    print(a)
    print((json5.dumps(a.serialize(), indent=4), 1))
