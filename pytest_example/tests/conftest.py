from learn.pytest_example import shape_circle, shape_rectangle, shape_square

import pytest


@pytest.fixture
def square():
    obj: shape_square.Square = shape_square.Square(8)
    yield obj
    del obj


@pytest.fixture
def circle():
    obj: shape_circle.Circle = shape_circle.Circle(5)
    yield obj
    del obj


@pytest.fixture
def rectangle():
    obj = shape_rectangle.Rectangle(8, 5)
    yield obj
    del obj
