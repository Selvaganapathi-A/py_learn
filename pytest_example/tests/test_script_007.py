from typing import Any, Callable

from learn.pytest_example import fibo

import pytest


def fake_fib_compute(n: int):
    return 9000


@pytest.fixture
def mocker_function(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(fibo, "fibbonocci_number", fake_fib_compute)


def test_fibo(mocker_function: Callable[..., Any]):
    assert fibo.fibbonocci_number(100) == 9000
