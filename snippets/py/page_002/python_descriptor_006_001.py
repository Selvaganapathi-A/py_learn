class InstanceLevelDescriptor:

    def __set_name__(self, cls, cls_name):
        self.cls_name = cls_name
        self.__record_keeper__ = dict()
        # self.cls = cls

    def __get__(self, instance, cls):
        print("get instance", cls)
        if instance in self.__record_keeper__:
            return self.__record_keeper__[instance]
        else:
            return None

    def __set__(self, instance, value):
        print("set instance", value)
        self.__record_keeper__[instance] = value
        instance.__dict__[self.cls_name] = (value if self.cls_name
                                            in instance.__dict__ else None)


class SomeClass:
    fc = InstanceLevelDescriptor()

    def __init__(self, value: None | str = None) -> None:
        self.fc = value


if __name__ == "__main__":
    i = SomeClass("one")
    ii = SomeClass("Two")
    iii = SomeClass("Three")

    print()
    print("before")

    print(i.fc)
    print(ii.fc)
    print(iii.fc)
    print()
    print()

    i.fc = "I"
    iii.fc = "VI"

    print()
    print()

    print("after")

    print(i.fc)
    print(ii.fc)
    print(iii.fc)
    pass
