from collections.abc import Callable
from typing import Any

from py_learn.pytest_example import shape_circle, shape_rectangle, shape_square


class TestRectangle:
    def setup_method(self, method: Callable[..., Any]):
        self.a = 8
        self.b = 5
        self.rectangle = shape_rectangle.Rectangle(self.a, self.b)

    def teardown_method(self, method: Callable[..., Any]):
        del self.a
        del self.b
        del self.rectangle

    def test_area(self):
        assert self.rectangle.area() == self.a * self.b

    def test_perimeter(self):
        assert self.rectangle.perimeter() == 2 * (self.a + self.b)

    def test_equlality(
        self,
        circle: shape_circle.Circle,
        rectangle: shape_rectangle.Rectangle,
        square: shape_square.Square,
    ):
        assert self.rectangle == rectangle
        assert self.rectangle != circle
        assert self.rectangle != square


def test_rectangle_area(rectangle: shape_rectangle.Rectangle):
    assert rectangle.area() == 40


def test_rectangle_perimeter(rectangle: shape_rectangle.Rectangle):
    assert rectangle.perimeter() == 26
