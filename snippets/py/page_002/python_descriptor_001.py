from typing import Type


class StringDescriptor:
    def __set_name__(self, owner: Type, name: str):
        print('StringDescriptor', 'set name', owner)
        self.property_name = name

    def __get__(self, instance: object, owner: Type):
        print('StringDescriptor', 'get', instance, owner)
        if instance is None:
            return self
        else:
            return instance.__dict__[self.property_name] or None

    def __set__(self, instance: object, value: str):
        print('StringDescriptor', 'set', instance.__dict__)
        if len(value) != 1:
            raise ValueError('Must be non empty string')
        instance.__dict__[self.property_name] = value


class Person:
    f_name = StringDescriptor()
    l_name = StringDescriptor()

    def __init__(self, f_name, l_name) -> None:
        print('Persion --init--')
        self.f_name = f_name
        self.l_name = l_name


if __name__ == '__main__':
    person = Person('g', 'o')
    print(person)
    print(person.f_name)
    print(person.l_name)
    person.f_name = ''
    print(person.f_name)
    print(person.l_name)
