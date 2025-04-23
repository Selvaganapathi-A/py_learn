from abc import ABCMeta, abstractmethod
from typing import override


class Fruit(metaclass=ABCMeta):

    @abstractmethod
    def taste(self, value: str) -> str:
        ...

    def color(self) -> str:
        return 'pale'

    @abstractmethod
    @staticmethod
    def size() -> str:
        ...


class Tomato(Fruit):

    @override
    def taste(self, value: str = '') -> str:
        return 'sour,' + value

    def color(self) -> str:
        return 'red'

    @override
    @staticmethod
    def size() -> str:
        # Can't Run Without instantiating this abstact method from parent class
        return 'squishy'


class Apple(Fruit):

    def taste(self, value: str = 'sweet'):
        return value

    @staticmethod
    def size() -> str:
        return 'small'


if __name__ == '__main__':
    apple = Apple()
    print('Apple', apple.taste())
    print('Apple', apple.color())
    tomato = Tomato()
    print('Tomato', tomato.taste('not So Sweet...'))
    print('Tomato', tomato.color())
