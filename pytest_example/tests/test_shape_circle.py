from typing import Any, Callable

import math

from learn.pytest_example import shape_circle, shape_rectangle, shape_square


class TestCircle:

    def setup_method(self, method: Callable[..., Any]):
        self.radius = 5
        self.circle = shape_circle.Circle(self.radius)

    def teardown_method(self, method: Callable[..., Any]):
        del self.radius
        del self.circle

    def test_area(self):
        assert self.circle.area() == (self.radius**2) * math.pi

    def test_perimeter(self):
        assert self.circle.perimeter() == 2 * math.pi * self.radius

    def test_equlality(self, circle: shape_circle.Circle,
                       rectangle: shape_rectangle.Rectangle,
                       square: shape_square.Square):
        assert self.circle == circle
        assert self.circle != rectangle
        assert self.circle != square


def test_circle_area(circle: shape_circle.Circle):
    expected = math.pi * 5 * 5
    assert circle.area() == expected


def test_circle_perimeter(circle: shape_circle.Circle):
    expected = math.pi * 2 * 5
    assert circle.perimeter() == expected
