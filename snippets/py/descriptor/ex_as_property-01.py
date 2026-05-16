from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from collections.abc import Callable


class MyProperty[T]:
    owner: type
    instance: object
    name: str
    storage_name: str

    function_getter: Callable[[Any], T] | None
    function_setter: Callable[[Any, T], None] | None
    function_deletter: Callable[[Any], None] | None

    def __init__(
        self,
        function_getter: Callable[[Any], T] | None = None,
        function_setter: Callable[[Any, T], None] | None = None,
        function_deletter: Callable[[Any], None] | None = None,
        /,
    ) -> None:
        self.function_getter = function_getter
        self.function_setter = function_setter
        self.function_deletter = function_deletter

    def __set_name__(self, owner: type, name: str) -> None:
        print('__set_name__', owner, name)
        self.owner = owner
        self.name = name
        self.storage_name = f'_{name}'

    def __get__(self, instance: object | None, owner: type) -> Self | T:
        print('__get__', instance, owner)
        if instance is None or self.function_getter is None:
            return self
        return self.function_getter(instance)

    def __set__(self, instance: object | None, value: T) -> None:
        print('__set__', instance, value)
        if self.function_setter is None:
            return
        self.function_setter(instance, value)

    def __delete__(self, instance: object | None) -> None:
        print('__delete__', instance)
        if self.function_deletter is None:
            return
        self.function_deletter(instance)

    def setter(self, function_setter: Callable[[Any, T], None]) -> Self:
        print('setter', self)
        self.function_setter = function_setter
        return self

    def getter(self, function_getter: Callable[[Any], T]) -> Self:
        print('getter', self)
        self.function_getter = function_getter
        return self

    def deleter(self, function_deletter: Callable[[Any], None]) -> Self:
        print('deleter', self)
        self.function_deletter = function_deletter
        return self


class Student:
    _name: str
    _age: int

    def __init__(self, name: str, age: int) -> None:
        print(f'Student Initializing {name=} {age=}.')
        self._name = name
        self._age = age
        print('Student Initialized.')

    @MyProperty[int]
    def age(self) -> int:  # pyright: ignore[reportRedeclaration]
        return self._age

    @age.setter
    def age(self, age: int) -> None:  # pyright: ignore[reportRedeclaration]
        min_age: int = 10
        max_age: int = 24
        if age < min_age or max_age < age:
            error_message = 'Valid age must be between 10 and 20'
            raise ValueError(error_message)
        self._age = age

    @age.deleter
    def age(self) -> None:
        print(self.__dict__)
        del self._age
        print(self.__dict__)

    @MyProperty
    def name(self) -> str:  # pyright: ignore[reportRedeclaration]
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value


if __name__ == '__main__':
    import sys

    sys.setrecursionlimit(16)

    denice = Student('Denice', 13)
    print()
    print('Age before', denice.age)
    denice.age = 24
    print('Age after', denice.age)
    print()

    del denice.age

    print('Before Name', denice.name)
    denice.name = 'Elizabeth'
    print('After Name', denice.name)
    print()

    ae: AttributeError

    try:
        print(denice.name, denice.age)
    except AttributeError as ae:
        print(ae)
