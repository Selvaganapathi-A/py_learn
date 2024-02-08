import time


class LazyProperty:
    def __init__(self, function):
        self.function = function
        self.name = function.__name__
        print(self.name)
        print(self.function)

    def __get__(self, object_, class_=None) -> object:
        print("get called", (object_, class_))
        object_.__dict__[self.name] = self.function(object_)
        return object_.__dict__[self.name]

    # def __set__(self, obj, value):
    #     print("in setter of lazy property.")
    #     print(obj, value)
    #     obj.__dict__[self.name] = value
    # pass

    # def __del__(self, *args, **kwargs):
    #     print("->", args)
    #     print("->", kwargs)


class DeepThought:
    @LazyProperty
    def meaning_of_life(self):
        time.sleep(1)
        return 42


if __name__ == "__main__":
    my_deep_thought_instance = DeepThought()
    print()
    print("*" * 80)
    for i in range(2):
        # print(my_deep_thought_instance.__dict__)
        print(my_deep_thought_instance.meaning_of_life)
        # print()
    print("*" * 80)
    print("End of Program")
