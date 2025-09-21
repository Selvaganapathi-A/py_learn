import sys
import time

import pytest

from py_learn.pytest_example import script_001


@pytest.mark.skip(reason='Feature not Implemented.')
def test_underdeveloped_feature(): ...


@pytest.mark.xfail(reason='Cannot Divide by zero')
def test_divides_zero():
    assert script_001.divides(8, 0) == float('inf')


@pytest.mark.skipif(
    sys.version_info > (3, 10, 0),
    reason='unsupported python version.',
)
def test_hi():
    assert 45 == int('45')


@pytest.mark.skipif(sys.platform != 'linux', reason='unsupported platform.')
def test_for_linux_platform():
    assert 45 == int('45')


@pytest.mark.slow
def test_slow_function():
    time.sleep(10)


@pytest.mark.speed
def test_fast_function(): ...


@pytest.mark.anyio
async def test_async_add():
    async def add(a: float, b: float):
        return a + b

    assert await add(1, 2) == 3
