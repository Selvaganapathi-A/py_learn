class Descriptor_As_Property:
    def __init__(self, func_get=None, func_set=None, func_del=None):
        self.func_get = func_get
        self.func_set = func_set
        self.func_del = func_del

    def __get__(self, obj, objtype=None):
        # print("called __get__ method", obj, objtype)
        # sys.exit(400)
        if obj is None:
            return self
        return self.func_get(obj)

    def __set__(self, obj, value):
        print('called __set__ method', obj, value)
        self.func_set(obj, value)

    def __delete__(self, obj):
        print('called __delete__ method', obj)
        self.func_del(obj)

    def setter(self, func_set):
        print('called setter method')
        return type(self)(self.func_get, func_set, self.func_del)

    def getter(self, func_get):
        print('called getter method')
        return type(self)(func_get, self.func_set, self.func_del)

    def deleter(self, func_del):
        print('called deleter method')
        return type(self)(self.func_get, self.func_set, func_del)


class Student:
    def __init__(self, name, age):
        self.name = name
        self._age = age

    @Descriptor_As_Property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if not 10 <= age <= 20:
            raise ValueError('Valid age must be between 10 and 20')
        self._age = age

    def __repr__(self):
        return 'Student name:%s, Age:%d' % (self.name, self.age)


if __name__ == '__main__':
    print()
    martin = Student('martin', 15)
    print()
    martha = Student('martha', 38)
    print()
    print(martin.age)
    print()
    martin.age = 57
    print()
    print(martin.age)
