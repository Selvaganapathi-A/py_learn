from typing import Self


class _Node[T]:
    __slots__: tuple[str, ...] = ("prev", "value")

    def __init__(self, value: T, prev: None | Self = None) -> None:
        self.value: T = value
        self.prev: Self | None = prev


class _StackIterator[T]:
    __slots__: tuple[str, ...] = ("_current",)

    def __init__(self, node: _Node[T] | None):
        self._current = node

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> T:
        if self._current is None:
            raise StopIteration
        value = self._current.value
        self._current: _Node[T] | None = self._current.prev
        return value


class Stack[T]:
    __slots__: tuple[str, ...] = ("_size", "_top")

    def __init__(self) -> None:
        self._size: int = 0
        self._top: None | _Node[T] = None

    def peek(self) -> T:
        if self._top is None:
            raise IndexError("Cannot peek empty stack.")
        return self._top.value

    def push(self, item: T, /) -> None:
        self._top = _Node(value=item, prev=self._top)
        self._size += 1

    def pop(self) -> T:
        if self._top is None:
            raise IndexError("Pop from empty stack.")
        value: T = self._top.value
        self._top = self._top.prev
        self._size -= 1
        return value

    def __bool__(self) -> bool:
        return self._top is not None

    def __iter__(self) -> _StackIterator[T]:
        return _StackIterator(self._top)

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"Stack(size={self._size})"
