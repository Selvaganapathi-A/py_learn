from typing import Any, Self

"""
Store Values in Descriptor Dictionary instead of instance's dictionary.
Which is not part of instance, but part of descriptor.
"""


class StringDescriptor:
    owner: type
    field_name: str
    storage_name: str
    object_store: dict[tuple[type, object, str], str]

    def __init__(self) -> None:
        print('Descriptor --init--')
        self.object_store = {}

    def __set_name__(self, owner: type, name: str) -> None:
        print(f'SET_NAME {owner=!r}, {name=!r}')
        self.owner = owner
        self.field_name = name
        self.storage_name = f'_{name}'

    def __get__(self, instance: object, owner: type) -> Self | Any | None:
        print(f'GET {instance=!r}, {owner=!r}')
        if instance is None:
            return self
        return self.object_store.get((owner, instance, self.storage_name))

    def __set__(self, instance: object, value: str) -> None:
        print(f'SET {instance=!r}, {value=!r}')
        if len(value.strip()) < 1:
            error_message = 'Must be non empty string'
            raise ValueError(error_message)
        self.object_store[self.owner, instance, self.storage_name] = value


class Person:
    first_name: StringDescriptor = StringDescriptor()
    last_name: StringDescriptor = StringDescriptor()

    def __init__(self, first_name: str, last_name: str) -> None:
        print('Persion --init--')
        self.first_name = first_name
        self.last_name = last_name


if __name__ == '__main__':
    print(Person.first_name)
    person = Person('James', 'Camera')
    print(person)
    print(person.first_name, person.last_name)
    person.__dict__['last_name'] = 'Micky'
    person.last_name = 'Micky'
    print(person)
    print(person.first_name, person.last_name)
    #
    # ! Below code raises error.
    person.first_name = '      '
    print(person.first_name, person.last_name)
