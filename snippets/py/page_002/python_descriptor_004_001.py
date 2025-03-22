from subprocess import run

run(("cls",), shell=True)


class MyDescriptor:
    def __set_name__(self, owner, name):
        # print("set name", "owner", owner)
        # print("set name", "name", name)
        self.name = name
        self.owner = owner

    def __get__(self, instance, instance_type):
        # print("get", self.owner, self.name)
        # print("get", instance, instance_type)
        # print(dir(instance))
        if instance:
            return instance.__dict__[self.name]
        return None

    def __set__(self, instance, value):
        # print("set", self.owner, self.name)
        # print("set", instance, value)
        instance.__dict__[self.name] = value
        # setattr(self.owner, self.name, value)
        # print(instance.__dict__)


class Foo:
    a = MyDescriptor()
    b = MyDescriptor()
    c = MyDescriptor()

    def __init__(self, a, b, c) -> None:
        # self.a = MyDescriptor2()
        self.a = a
        self.b = b
        self.c = c


print("=" * 10)
# Foo.a = 12
# Foo.b = 13
# Foo.c = 15
print("=" * 10)
print("=" * 10)
#
oa = Foo(1, 2, 3)
print(oa.a)
print(oa.b)
print(oa.c)
print("=" * 10)
print("-" * 80)
oa.a = 1
oa.b = 2
oa.c = 4
print(oa.a)
print(oa.b)
print(oa.c)
print("*" * 80)
ob = Foo(4, 5, 6)
print(ob.a)
print(ob.b)
print(ob.c)
print("-" * 80)
ob.a = 3
ob.b = 7
ob.c = 11
print(oa.a)
print(oa.b)
print(oa.c)
print("." * 80)
print(ob.a)
print(ob.b)
print(ob.c)
print("=" * 10)
print("*" * 80)
oc = Foo(7, 8, 9)
print(oc.a)
print(oc.b)
print(oc.c)
print("-" * 80)
oc.a = 13
oc.b = 17
oc.c = 19
print(oa.a)
print(oa.b)
print(oa.c)
print("." * 80)
print(ob.a)
print(ob.b)
print(ob.c)
print("." * 80)
print(oc.a)
print(oc.b)
print(oc.c)
print("*" * 80)
