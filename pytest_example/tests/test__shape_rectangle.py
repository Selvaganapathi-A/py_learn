from py_learn.pytest_example import shape_circle, shape_rectangle, shape_square


class TestRectangle:
    def setup_method(self):
        self.a = 8
        self.b = 5
        self.rectangle = shape_rectangle.Rectangle(self.a, self.b)

    def teardown_method(self):
        del self.a
        del self.b
        del self.rectangle

    def test__area(self):
        assert self.rectangle.area() == self.a * self.b

    def test__perimeter(self):
        assert self.rectangle.perimeter() == 2 * (self.a + self.b)

    def test__equlality(
        self,
        circle: shape_circle.Circle,
        rectangle: shape_rectangle.Rectangle,
        square: shape_square.Square,
    ):
        assert hash(self.rectangle) != hash(rectangle)
        assert self.rectangle == rectangle
        assert self.rectangle != circle
        assert self.rectangle != square


def test__rectangle_area(rectangle: shape_rectangle.Rectangle):
    expected_value = 40
    assert expected_value == rectangle.area()


def test__rectangle_perimeter(rectangle: shape_rectangle.Rectangle):
    expected_value = 26
    assert expected_value == rectangle.perimeter()
