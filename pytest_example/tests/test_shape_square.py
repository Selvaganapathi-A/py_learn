from collections.abc import Callable
from typing import Any

from py_learn.pytest_example import shape_circle, shape_rectangle, shape_square


class TestSquare:
    def setup_method(self, method: Callable[..., Any]):
        self.side = 8
        self.square = shape_square.Square(self.side)

    def teardown_method(self, method: Callable[..., Any]):
        del self.side
        del self.square

    def test_area(self):
        assert self.square.area() == self.side**2

    def test_perimeter(self):
        assert self.square.perimeter() == self.side * 4

    def test_equlality(
        self,
        circle: shape_circle.Circle,
        rectangle: shape_rectangle.Rectangle,
        square: shape_square.Square,
    ):
        assert self.square == square
        assert self.square != circle
        assert self.square != rectangle


def test_square_area(square: shape_square.Square):
    assert square.area() == 64


def test_square_perimeter(square: shape_square.Square):
    assert square.perimeter() == 32
