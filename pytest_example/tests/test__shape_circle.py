import math

from py_learn.pytest_example import shape_circle, shape_rectangle, shape_square


class TestCircle:
    def setup_method(self):
        self.radius = 5
        self.circle = shape_circle.Circle(self.radius)

    def teardown_method(self):
        del self.radius
        del self.circle

    def test__area(self):
        assert self.circle.area() == (self.radius**2) * math.pi

    def test__perimeter(self):
        assert self.circle.perimeter() == 2 * math.pi * self.radius

    def test__equlality(
        self,
        circle: shape_circle.Circle,
        rectangle: shape_rectangle.Rectangle,
        square: shape_square.Square,
    ):
        assert hash(self.circle) != hash(circle)
        assert self.circle is not circle
        assert self.circle != rectangle
        assert self.circle != square
        assert self.circle == circle


def test__circle_area(circle: shape_circle.Circle):
    expected = math.pi * 5 * 5
    assert circle.area() == expected


def test__circle_perimeter(circle: shape_circle.Circle):
    expected = math.pi * 2 * 5
    assert circle.perimeter() == expected
