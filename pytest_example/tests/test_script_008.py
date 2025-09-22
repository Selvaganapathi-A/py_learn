from unittest.mock import MagicMock, patch

from py_learn.pytest_example import fibbonocci, shape_square


@patch('py_learn.pytest_example.fibo.fibbonocci_number')
def test_function(mock_fibbonocci: MagicMock):
    mock_fibbonocci.return_value = 123789
    assert fibbonocci.fibbonocci_number(800) == 123789


@patch('py_learn.pytest_example.shape_square.Square.perimeter')
def test_square_perimeter(mock_square: MagicMock):
    mock_square.return_value = 980
    assert shape_square.Square(900).perimeter() == 980


@patch('py_learn.pytest_example.shape_square.Square.area')
def test_square_area(mock_square: MagicMock):
    mock_square.return_value = 441
    assert shape_square.Square(900).area() == 441
