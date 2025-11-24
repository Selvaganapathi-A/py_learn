from typing import Any, cast, Self, TypeVar
import logging


class Ok[T]:
    def __init__(self, value: T) -> None:
        pass


class Result[V, E: BaseException]:
    def __init__(
        self,
        value: V | None = None,
        error: E | None = None,
        is_err: bool = False,
    ) -> None:
        self._value: V | None = value
        self._error: E | None = error
        self._is_err: bool = is_err
        self._is_ok: bool = not is_err

    @property
    def result(self) -> V:
        return cast(V, self._value)

    @property
    def error(self) -> E:
        return cast(E, self._error)

    def is_ok(self) -> bool:
        return self._is_ok

    def is_err(self) -> bool:
        return self._is_err

    @staticmethod
    def Ok(value: V) -> 'Result':
        return Result(value, is_err=False)

    @staticmethod
    def Err(error: E) -> 'Result':
        return Result(error=error, is_err=True)


T = TypeVar('T', float, str)


def add(a: T | None, b: T | None):
    if a is None:
        return Result.Err(ValueError('a is none', a))
    if b is None:
        return Result.Err(ValueError('b is none', b))
    return Result.Ok(a + b)


logging.basicConfig(format='{levelname: >10}-{message}', style='{')

c = add(1, None)
if c.is_ok():
    print(c.result)
else:
    logging.exception(c.error)
