from typing import NoReturn


def addition(a: float, b: float, /) -> float:
    return a + b


def greet(string: str) -> str:
    return 'Howdy! ' + string


def greet_custom(string: str, greet_string: str) -> str:
    return greet_string + ' ' + string


def raise_error() -> NoReturn:
    raise ZeroDivisionError(1, 0)


def divides(a: float, b: float, /) -> float:
    return a / b
