from typing import Self


class PositiveNumber[T](int):
    def __set_name__(self, __class: type[T], name: str):
        print(__class, name)
        self.__class = __class
        self.object_name = name

    def __get__(self, __class_instance: T, __class: type[T]) -> int:
        # print('called get', (__class_instance, __class))
        return __class_instance.__dict__.get(self.object_name, 0)
        return (
            __class_instance.__dict__[self.object_name]
            if self.object_name in __class_instance.__dict__
            else None
        )

    def __set__(self, __object_instance: T, __object_value: int):
        print('called set with value', __object_instance, __object_value)
        if __object_value < 1:
            raise ValueError('Must be Positive Integer', __object_value)
        __object_instance.__dict__[self.object_name] = __object_value


class Apple:
    sold_apples: PositiveNumber[Self] = PositiveNumber[Self]()

    def __init__(self, value: int) -> None:
        self.sold_apples: PositiveNumber[Self] = value


if __name__ == '__main__':
    a = Apple(109)
    print(a.sold_apples)
    try:
        for x in range(4, 20):
            a.sold_apples -= x
            print(a.sold_apples)
    except ValueError as ve:
        print(ve.args)
    print(a.sold_apples)
