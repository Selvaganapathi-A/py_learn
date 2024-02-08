from typing import Self


class Node[T]:
    def __init__(self, value: T, prev: None | Self = None) -> None:
        self.value: T = value
        self.prev: Self | None = prev


class Stack[T]:
    def __init__(self) -> None:
        self.__size: int = 0
        self.__top: None | Node[T] = None

    @property
    def isEmpty(self) -> bool:
        return self.__top is None

    def peek(self) -> T:
        if self.__top is None:
            raise ValueError("Empty Stack")
        else:
            return self.__top.value

    def insert(self, __value: T, /) -> None:
        self.__size += 1
        node = Node(value=__value, prev=self.__top)
        self.__top = node

    def pop(self):
        if self.__top is None:
            raise ValueError("Empty Stack")
        else:
            self.__size -= 1
            value: T = self.__top.value
            self.__top = self.__top.prev
            return value

    def __iter__(self) -> Self:
        self.ptr: Node[T] | None = self.__top
        return self

    def __next__(self) -> T:
        if self.ptr is None:
            raise StopIteration()
        return_value: T = self.ptr.value
        self.ptr = self.ptr.prev
        return return_value
