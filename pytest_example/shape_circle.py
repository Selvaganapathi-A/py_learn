from typing import override

import math

from learn.pytest_example.shape import Shape


class Circle(Shape):

    def __init__(self, radius: float) -> None:
        super().__init__()
        self.radius = radius

    @override
    def area(self):
        return math.pi * self.radius * self.radius

    @override
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius

    @override
    def __eq__(self, __value: object, /) -> bool:
        if isinstance(__value, Circle):
            return self.radius == __value.radius
        return False
