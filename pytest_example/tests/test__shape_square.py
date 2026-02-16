from py_learn.pytest_example import shape_circle, shape_rectangle, shape_square


class TestSquare:
    def setup_method(self):
        self.side = 8
        self.square = shape_square.Square(self.side)

    def teardown_method(self):
        del self.side
        del self.square

    def test__area(self):
        assert self.square.area() == self.side**2

    def test__perimeter(self):
        assert self.square.perimeter() == self.side * 4

    def test__equlality(
        self,
        circle: shape_circle.Circle,
        rectangle: shape_rectangle.Rectangle,
        square: shape_square.Square,
    ):
        assert hash(self.square) != hash(square)
        assert self.square == square
        assert self.square != circle
        assert self.square != rectangle


def test__square_area(square: shape_square.Square):
    expected_value = 64
    assert expected_value == square.area()


def test__square_perimeter(square: shape_square.Square):
    expected_value = 32
    assert expected_value == square.perimeter()
