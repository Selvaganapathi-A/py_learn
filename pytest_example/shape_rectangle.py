from typing import override

from py_learn.pytest_example.shape import Shape


class Rectangle(Shape):

    def __init__(self, a: float, b: float) -> None:
        super(Rectangle, self).__init__()
        self.a = a
        self.b = b

    @override
    def area(self):
        return self.a * self.b

    @override
    def perimeter(self) -> float:
        return 2 * (self.a + self.b)

    @override
    def __eq__(self, __value: object, /) -> bool:
        if isinstance(__value, Rectangle):
            return self.a == __value.a and self.b == __value.b
        return False
