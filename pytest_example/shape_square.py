from typing import override

from py_learn.pytest_example.shape import Shape


class Square(Shape):

    def __init__(self, side: float) -> None:
        super().__init__()
        self.a = side

    @override
    def area(self):
        return self.a**2

    @override
    def perimeter(self) -> float:
        return self.a * 4

    @override
    def __eq__(self, __value: object, /) -> bool:
        if isinstance(__value, Square):
            return self.a == __value.a
        return False
