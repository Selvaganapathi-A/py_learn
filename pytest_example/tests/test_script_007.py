from typing import Any, Callable

import pytest

from py_learn.pytest_example import fibo


def fake_fib_compute(n: int):
    return 9000


@pytest.fixture
def mocker_function(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(fibo, "fibbonocci_number", fake_fib_compute)


def test_fibo(mocker_function: Callable[..., Any]):
    assert fibo.fibbonocci_number(100) == 9000
