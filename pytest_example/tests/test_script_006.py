from py_learn.pytest_example import script_001, shape_square

import pytest


@pytest.mark.parametrize("a, b, result", [(1, 2, 3), (3, 4, 7), (5, 6, 11),
                                          (7, 8, 15), (9, 10, 19),
                                          (11, 12, 23), (13, 14, 27),
                                          (15, 16, 31), (17, 18, 35),
                                          (19, 20, 39), (21, 22, 43),
                                          (23, 24, 47), (25, 26, 51),
                                          (27, 28, 55), (29, 30, 59),
                                          (31, 32, 63), (33, 34, 67),
                                          (35, 36, 71), (37, 38, 75),
                                          (39, 40, 79)])
def test_addition(a: float, b: float, result: float):
    assert script_001.addition(a, b) == result


@pytest.mark.parametrize("side, result", [(1, 1), (2, 4), (3, 9), (4, 16),
                                          (5, 25), (6, 36), (7, 49), (8, 64),
                                          (9, 81), (10, 100), (11, 121),
                                          (12, 144), (13, 169), (14, 196),
                                          (15, 225), (16, 256), (17, 289),
                                          (18, 324), (19, 361), (20, 400)])
def test_shape_square_area(side: float, result: float):
    assert shape_square.Square(side).area() == result
