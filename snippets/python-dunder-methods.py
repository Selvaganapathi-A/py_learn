import operator
from types import UnionType
from typing import Any, Self

from rich import print


class SomeClass(object):
    def __init__(self, worth: float = 0) -> None:
        self.__worth = worth

    def __add__(self, __value: Self) -> Self:
        print('"add" Method')
        ...

    def __sub__(self, __value: Self) -> bool:
        print('"sub" Method')
        ...

    def __mul__(self, __value: Self) -> bool:
        print('"mul" Method')
        ...

    def __matmul__(self, __value: Self) -> bool:
        print('"MatMul" Method')
        ...

    def __truediv__(self, __value: Self) -> bool:
        print('"truediv" Method')
        ...

    def __floordiv__(self, __value: Self) -> bool:
        print('"floordiv" Method')
        ...

    def __mod__(self, __value: Self) -> bool:
        print('"mod" Method')
        ...

    def __pow__(self, __value: Self) -> bool:
        print('"pow" Method')
        ...

    def __and__(self, __value: Self) -> bool:
        print('"and" Method')
        ...

    def __or__(self, __value: Self) -> bool:
        print('"or" Method')
        ...

    def __xor__(self, __value: Self) -> bool:
        print('"xor" Method')
        ...

    def __invert__(self) -> bool:
        print('"invert" Method')
        ...

    def __lshift__(self, __value: Self) -> bool:
        print('"lshift" Method')
        ...

    def __rshift__(self, __value: Self) -> bool:
        print('"rshift" Method')
        ...

    def __eq__(self, __value: Self) -> bool:
        print('"eq" Method')
        ...

    def __ne__(self, __value: Self) -> bool:
        print('"ne" Method')
        ...

    def __lt__(self, __value: Self) -> bool:
        print('"lt" Method')
        ...

    def __le__(self, __value: Self) -> bool:
        print('"le" Method')
        ...

    def __gt__(self, __value: Self) -> bool:
        print('"gt" Method')
        ...

    def __ge__(self, __value: Self) -> bool:
        print('"ge" Method')
        ...

    def __iadd__(self, __value: Self) -> bool:
        print('"iadd" Method')
        ...

    def __isub__(self, __value: Self) -> bool:
        print('"isub" Method')
        ...

    def __imul__(self, __value: Self) -> bool:
        print('"imul" Method')
        ...

    def __itruediv__(self, __value: Self) -> bool:
        print('"itruediv" Method')
        ...

    def __ifloordiv__(self, __value: Self) -> bool:
        print('"ifloordiv" Method')
        ...

    def __imod__(self, __value: Self) -> bool:
        print('"imod" Method')
        ...

    def __ipow__(self, __value: Self) -> bool:
        print('"ipow" Method')
        ...

    def __not__(self) -> bool:
        print('"not" Method')
        ...

    def __contains__(self, __value: Self) -> bool:
        print('"contains" Method')
        ...

    def __getitem__(self, __value: Self) -> bool:
        print('"getitem" Method')
        print(__value)
        ...

    def __setitem__(self, __value: Self) -> bool:
        print('"setitem" Method')
        ...

    def __delitem__(self, __value: Self) -> bool:
        print('"delitem" Method')
        ...

    def __call__(self, __value: Self) -> bool:
        print('"call" Method')
        ...

    def __enter__(self, __value: Self) -> bool:
        print('"enter" Method')
        ...

    def __exit__(self, __value: Self) -> bool:
        print('"exit" Method')
        ...

    def __aenter__(self, __value: Self) -> bool:
        print('"aenter" Method')
        ...

    def __aexit__(self, __value: Self) -> bool:
        print('"aexit" Method')
        ...

    def __iter__(self, __value: Self) -> bool:
        print('"iter" Method')
        ...

    def __next__(self, __value: Self) -> bool:
        print('"next" Method')
        ...

    def __aiter__(self, __value: Self) -> bool:
        print('"aiter" Method')
        ...

    def __anext__(self, __value: Self) -> bool:
        print('"anext" Method')
        ...

    def __await__(self, __value: Self) -> bool:
        print('"await" Method')
        ...

    def __bool__(self) -> bool:
        print('"bool" Method')
        return True

    def __neg__(self) -> bool:
        print('"neg" Method')
        return 'Negate fn'

    def __pos__(self) -> bool:
        print('"pos" Method')
        return True

    def __len__(self):
        return 1020
