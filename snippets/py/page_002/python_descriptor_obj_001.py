# descriptors4.py
class OneDigitNumericValue:

    def __init__(self, *name):
        print(name)
        self.name = name

    def __get__(self, obj, type=None) -> object:
        return obj.__dict__.get(self.name) or 0

    def __set__(self, obj, value) -> None:
        obj.__dict__[self.name] = value


class Foo:
    event_id = OneDigitNumericValue('number')
    people_id = OneDigitNumericValue('number')


my_foo_object = Foo()
my_second_foo_object = Foo()
#
my_second_foo_object.people_id = 76
print(my_foo_object.event_id)
my_foo_object.event_id = 879
print(my_second_foo_object.event_id)
my_third_foo_object = Foo()
print(my_third_foo_object.event_id)
print(my_foo_object.event_id)
print(my_foo_object.people_id)
print()
print(my_second_foo_object.event_id)
print(my_second_foo_object.people_id)
