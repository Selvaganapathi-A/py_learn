from unittest.mock import MagicMock, patch

from py_learn.pytest_example import fibbonocci, shape_square


@patch("py_learn.pytest_example.fibbonocci.fibbonocci_number")
def test__function(mock_fibbonocci: MagicMock):
    mock_fibbonocci.return_value = 123789
    expected_value = 123789
    assert expected_value == fibbonocci.fibbonocci_number(800)


@patch("py_learn.pytest_example.shape_square.Square.perimeter")
def test__square_perimeter(mock_square: MagicMock):
    mock_square.return_value = 980
    expected_value = 980
    assert expected_value == shape_square.Square(900).perimeter()


@patch("py_learn.pytest_example.shape_square.Square.area")
def test__square_area(mock_square: MagicMock):
    mock_square.return_value = 441
    expected_value = 441
    assert expected_value == shape_square.Square(900).area()
