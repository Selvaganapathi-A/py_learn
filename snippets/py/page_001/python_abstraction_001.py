from abc import ABCMeta, abstractmethod, abstractstaticmethod


class Fruit(metaclass=ABCMeta):
    @abstractmethod
    def taste(self, value: str) -> str:
        print("taste of fruit is", value)
        return "goat"

    def color(self) -> str:
        print("pale")
        return "pale"

    @abstractstaticmethod
    def size():
        return "large"


class Tomato(Fruit):
    def taste(self, value: str) -> str:
        return super().taste(value)

    def color(self) -> str:
        return "red"

    @staticmethod
    def size() -> str:
        # Can't Run Without instantiating this abstact method from parent class
        return "squishy"


class Apple(Fruit):
    def taste(self, value: str = "sweet"):
        return super().taste(value)

    @staticmethod
    def size() -> str:
        return "small"


if __name__ == "__main__":
    apple = Apple()
    apple.taste()
    apple.color()

    tomato = Tomato()
    tomato.taste("not So Sweet...")
    tomato.color()
