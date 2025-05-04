from decimal import Decimal
from typing import overload

@overload
def combine(a: int, b: int) -> int:
    ...


@overload
def combine(a: float, b: float) -> float:
    ...


@overload
def combine(a: list[int], b: list[int]) -> list[int]:
    ...


@overload
def combine(a: Decimal, b: Decimal) -> Decimal:
    ...


@overload
def combine(a: str, b: str) -> str:
    ...


def combine(a, b):
    """return the combined value of args."""
