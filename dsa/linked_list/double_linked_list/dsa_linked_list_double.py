from collections.abc import Generator
from typing import Self


class Node[T]:
    def __init__(self, data: T) -> None:
        self.data: T = data
        self.previous_node: Self | None = None
        self.next_node: Self | None = None

    def __repr__(self) -> str:
        return f'Node(data = {self.data})'


class LinkedList[T]:
    def __init__(self) -> None:
        self.head_node: Node[T] | None = None
        self.tail_node: Node[T] | None = self.head_node
        self.__length: int = 0

    def append(self, data: T):
        new_node = Node[T](data=data)
        if self.head_node is None:
            self.head_node = new_node
            self.tail_node = self.head_node
            self.__length += 1
        else:
            new_node.previous_node = self.tail_node
            if self.tail_node is not None:
                self.tail_node.next_node = new_node
            self.tail_node = new_node
            self.__length += 1

    def prepend(self, data: T):
        new_node = Node[T](data=data)
        if self.head_node is None:
            self.head_node = new_node
            self.tail_node = self.head_node
            self.__length += 1
        else:
            new_node.next_node = self.head_node
            self.head_node.previous_node = new_node
            self.head_node = new_node
            self.__length += 1

    def view(self) -> Generator[T, None, None]:
        if self.head_node is not None:
            current_node: Node[T] | None = self.head_node
            while current_node is not None:
                yield current_node.data
                current_node = current_node.next_node

    def view_backward(self) -> Generator[T, None, None]:
        if self.tail_node is not None:
            current_node: Node[T] | None = self.tail_node
            while current_node is not None:
                yield current_node.data
                current_node = current_node.previous_node

    def remove_first(self) -> T:
        if self.head_node is None:
            raise ValueError("Can't perform operations on Empty List")
        if self.head_node is self.tail_node:
            self.tail_node = None
        current_node = self.head_node
        self.head_node = self.head_node.next_node
        if self.head_node is not None:
            self.head_node.previous_node = None
        return current_node.data

    def remove_last(self) -> T:
        if self.tail_node is None:
            raise ValueError("Can't perform operations on Empty List")
        current_node = self.tail_node
        self.tail_node = current_node.previous_node
        if self.tail_node is not None:
            self.tail_node.next_node = None
        if current_node is self.head_node:
            self.head_node = None
        return current_node.data

    @property
    def length(self) -> int:
        return self.__length

    @length.setter
    def length(self, value: int):
        raise ValueError("Can't set Length.")


def main():
    import string

    linkedList: LinkedList[str] = LinkedList[str]()
    people = string.ascii_uppercase
    for person in people:
        linkedList.append(person)
    linkedList.remove_last()
    linkedList.remove_last()
    linkedList.remove_last()
    linkedList.remove_last()
    linkedList.remove_last()
    linkedList.remove_last()
    linkedList.remove_last()
    linkedList.remove_last()
    linkedList.remove_last()
    linkedList.remove_last()
    linkedList.remove_first()
    linkedList.remove_first()
    linkedList.remove_first()
    linkedList.remove_first()
    linkedList.remove_first()
    linkedList.remove_first()
    linkedList.remove_first()
    linkedList.remove_first()
    linkedList.remove_first()
    linkedList.remove_first()
    # print(" Show List ".center(60, "-"))
    # for person in linkedList.view():
    #     print(person, end=", ")
    # print(" End of List ".center(60, "-"))
    # print(" Show List ".center(60, "-"))
    # for person in linkedList.view_backward():
    #     print(person, end=", ")
    # print(" End of List ".center(60, "-"))
    # print("Removed First Node", linkedList.remove_first())
    # print("Removed First Node", linkedList.remove_first())
    # print("Removed First Node", linkedList.remove_first())
    # print("Removed First Node", linkedList.remove_first())
    # print("Removed First Node", linkedList.remove_first())
    # print("Removed First Node", linkedList.remove_first())
    # print("Removed Last Node", linkedList.remove_last())
    # print("Removed Last Node", linkedList.remove_last())
    # print("Removed Last Node", linkedList.remove_last())
    # print(linkedList.remove_last())
    # print(linkedList.remove_last())
    # print(linkedList.remove_last())
    # print(linkedList.remove_last())
    # print(linkedList.remove_last())
    # print(linkedList.remove_last())
    # print(linkedList.remove_last())
    # print(linkedList.remove_last())
    #
    # print("after io operations")
    # for person in linkedList.view():
    #     print(person, end=", ")


if __name__ == '__main__':
    import timeit

    print(timeit.timeit(main, number=10000))
    # main()
