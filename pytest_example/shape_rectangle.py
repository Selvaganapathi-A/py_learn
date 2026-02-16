from typing import override

from py_learn.pytest_example.shape import Shape


class Rectangle(Shape):
    def __init__(self, a: float, b: float) -> None:
        super().__init__()
        self.a: float = a
        self.b: float = b

    @override
    def area(self) -> float:
        return self.a * self.b

    @override
    def perimeter(self) -> float:
        return 2 * (self.a + self.b)

    @override
    def __eq__(self, __value: object, /) -> bool:
        if isinstance(__value, Rectangle):
            return self.a == __value.a and self.b == __value.b
        return False

    def __hash__(self) -> int:
        return super().__hash__()
