from collections.abc import Callable
from typing import Any

import pytest

from py_learn.pytest_example import fibbonocci


def fake_fib_compute(n: int):
    return 9000


@pytest.fixture
def mocker_function(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(fibbonocci, 'fibbonocci_number', fake_fib_compute)


def test_fibo(mocker_function: Callable[..., Any]):
    assert fibbonocci.fibbonocci_number(100) == 9000
