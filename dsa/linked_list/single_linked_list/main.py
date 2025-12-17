from timeit import timeit

from icecream import ic

from py_learn.dsa.linked_list.single_linked_list.dsa_linked_list_single import (
    Node, Singly_Linked_List)


def find_middle[T](ll: Singly_Linked_List[T]):
    if ll.head is None or ll.head.next is None:
        return
    slow_ptr: Node[T] | None = ll.head
    fast_ptr: Node[T] | None
    if slow_ptr is not None and slow_ptr.next is not None:
        fast_ptr = slow_ptr.next.next
    else:
        fast_ptr = None
    while fast_ptr and slow_ptr:
        fast_ptr = fast_ptr.next.next if fast_ptr.next else None
        slow_ptr = slow_ptr.next
    return slow_ptr


def main_1():
    li = Singly_Linked_List[str]()
    for x in range(0, 7, 1):
        li.append(chr(x + 65))
    for x in li.view():
        print(x)
    ic(find_middle(li))


def main():
    import string

    linked_list: Singly_Linked_List[str] = Singly_Linked_List[str]()
    # print(linked_list.length)
    for x in string.ascii_uppercase:
        linked_list.append(x)
    # print(" Show list ".center(60, "-"))
    # for a in linked_list.view():
    #     print(a, end=", ")
    # print(" Show list ".center(60, "-"))
    # linked_list.reverse()
    # # print("Show Reverse list".center(60, "-"))
    # # for a in linked_list.view():
    # #     print(a, end=", ")
    # #
    # # print("Show Reverse list".center(60, "-"))
    # linked_list.remove("Z")
    # linked_list.remove("V")
    # linked_list.remove("W")
    # linked_list.remove("Y")
    # linked_list.remove("X")
    # linked_list.remove("arul")
    # print("After removing list".center(60, "-"))
    # for a in linked_list.view():
    #     print(a, end=", ")
    # print("After removing list".center(60, "-"))


if __name__ == '__main__':
    print(timeit(main, number=100000))
    print(timeit(main_1, number=100000))
    # main()
