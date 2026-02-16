from py_learn.pytest_example import fibbonocci


def test__fibbonocci_number():
    expected_value = 55
    assert fibbonocci.fibbonocci_number(40) == expected_value


def test__fibbonocci_sequence():
    expected_value = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    got = list(fibbonocci.fibbonocci_sequence(100))
    assert expected_value == got
