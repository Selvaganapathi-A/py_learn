import pytest

from py_learn.pytest_example import fibbonocci


def test__monkey_patched_function(monkeypatch: pytest.MonkeyPatch):
    def fake_fib_compute(arg: int, /):  # noqa: ARG001
        return 9000

    monkeypatch.setattr(fibbonocci, "fibbonocci_number", fake_fib_compute)
    expected_result = 9000
    assert expected_result == fibbonocci.fibbonocci_number(100)
