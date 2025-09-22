from collections.abc import Generator
from typing import NoReturn, Self


# * Node
#
class Node[T]:
    def __init__(self, data: T) -> None:
        self.data: T = data
        self.next: Self | None = None

    def __repr__(self) -> str:
        return f'{self.data}'


# * Single Linked List
#
class Singly_Linked_List[T]:
    def __init__(self) -> None:
        self.head: Node[T] | None = None
        self.__length: int = 0

    def append(self, data: T):
        new_node: Node[T] = Node(data=data)
        if self.head is None:
            self.head = new_node
        else:
            current_node: Node[T] = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = new_node
        self.__length += 1

    def view(self) -> Generator[T, None, None]:
        if self.head is None:
            return
        current_node: Node[T] | None = self.head
        while current_node is not None:
            yield current_node.data
            current_node = current_node.next
        del current_node

    def reverse(self):
        if self.head is None or self.head.next is None:
            return
        previous_node: Node[T] | None = None
        current_node: Node[T] | None = self.head
        temp: Node[T] | None = None
        while current_node is not None:
            temp: Node[T] | None = current_node.next
            current_node.next = previous_node
            previous_node = current_node
            current_node = temp
        self.head = previous_node

    def remove(self, value: T) -> bool:
        if self.head is None:
            return False
        else:
            prev: Node[T] | None = None
            current_node: Node[T] | None = self.head
            while current_node:
                if current_node.data == value:
                    if prev is None:
                        self.head = current_node.next
                        del current_node
                        return True
                    else:
                        prev.next = current_node.next
                        del current_node
                        return True
                else:
                    prev = current_node
                    current_node = current_node.next
            else:
                raise ValueError(value, 'Not in List.')

    @property
    def length(self) -> int:
        return self.__length

    @length.setter
    def length(self, value: int) -> NoReturn:
        raise ValueError("Can't set Length.")
