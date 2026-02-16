import asyncio
import sys
import time

import pytest

from py_learn.pytest_example import script_001


@pytest.mark.skip(reason="Feature not Implemented.")
def test__underdeveloped_feature():
    error_message = "⚠️ `under_developed_feature()` not Implemented yet!"
    raise NotImplementedError(error_message)


@pytest.mark.xfail(reason="Cannot Divide by zero")
def test__divides_zero():
    assert script_001.divides(8, 0) == float("inf")


@pytest.mark.skipif(
    sys.version_info < (3, 10, 0),
    reason="unsupported python version.",
)
def test__hi():
    expected_value = 45
    assert expected_value == int("45")


@pytest.mark.skipif(sys.platform != "linux", reason="unsupported platform.")
def test__for_linux_platform():
    expected_value = 45
    assert expected_value == int("45")


@pytest.mark.slow
def test__slow_function():
    time.sleep(10)


@pytest.mark.speed
def test__fast_function(): ...
@pytest.mark.anyio
async def test__async_add():
    async def samba(a: float, b: float):
        await asyncio.sleep(1)
        return a * b / (a + b)

    expected_result = 3
    assert expected_result == await samba(4, 12)
