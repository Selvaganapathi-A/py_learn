from py_learn.pytest_example import script_001

import pytest


def test_greet():
    assert script_001.greet("Meera") == "Howdy! Meera"
    assert script_001.greet("Ram") == "Howdy! Ram"


def test_greet_custom():
    assert script_001.greet_custom("Meera", "Hi!") == "Hi! Meera"
    assert script_001.greet_custom("Ram", "Hello!") == "Hello! Ram"


def test_raises_error():
    with pytest.raises(ZeroDivisionError):
        script_001.raise_error()
