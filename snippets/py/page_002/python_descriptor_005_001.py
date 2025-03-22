# descriptors2.py
class OneDigitNumericValue:
    def __init__(self):
        self.value = 0

    def __get__(self, obj, type=None) -> object:
        print("get", obj, type)
        return self.value

    def __set__(self, obj, value) -> None:
        print("set", obj, value)
        if value > 9 or value < 0 or int(value) != value:
            raise AttributeError("The value is invalid", value)
        self.value = value


class Foo:
    number = OneDigitNumericValue()


my_foo_object = Foo()
my_second_foo_object = Foo()
my_foo_object.number = 93
print(my_foo_object.number)
print(my_second_foo_object.number)
my_third_foo_object = Foo()
print(my_third_foo_object.number)
# class ClassLevelDescriptor:
#     def __set_name__(self, cls, cls_name):
#         self.cls_name = cls_name
#         self.cls = cls
#     def __get__(self, instance, cls):
#         print("get", self, instance, cls)
#         return self.cls.__dict__[self.cls_name]
#     def __set__(self, instance, value):
#         print("set", self, instance, value)
#         # help(setattr)
#         setattr(self.cls, self.cls_name, value)
# class SomeClass:
#     fc = ClassLevelDescriptor()
#     def __init__(self, value: None | str = None) -> None:
#         self.fc = value
# if __name__ == "__main__":
#     i = SomeClass("one")
#     ii = SomeClass("Two")
#     iii = SomeClass("Three")
#     print()
#     print("before")
#     print(i.fc)
#     print(ii.fc)
#     print(iii.fc)
#     i.fc = "I"
#     iii.fc = "VI"
#     print()
#     print("after")
#     print(iii.fc)
#     print(ii.fc)
#     print(i.fc)
#     print()
#     i.fc = "OI"
#     print(SomeClass.fc)
#     print(SomeClass.fc)
#     pass
