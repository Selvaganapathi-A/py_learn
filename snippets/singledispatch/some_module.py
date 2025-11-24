from decimal import Decimal
from functools import singledispatch


@singledispatch
def combine(a, b):
    return a + b


@combine.register
def _(a: int, b: int) -> int:
    return a + b


@combine.register
def _(a: str, b: str) -> str:
    return a + b


@combine.register
def _(a: list, b: list) -> list:
    return a + b


@combine.register
def _(a: Decimal, b: Decimal) -> Decimal:
    return a + b
