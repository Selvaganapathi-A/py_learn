from typing import Any, Self, Type


class Robot:
    __identity__: int = 0

    def __new__(cls: type[Self], *args: Any, **kwargs: Any) -> Self:
        cls.__identity__ += 1
        return super().__new__(cls)

    def __init__(self, name: str = 'Pear') -> None:
        self.f_name = name

    @property
    def objects_created(self):
        return self.__identity__

    @classmethod
    def instances(cls):
        return cls.__identity__

    def __repr__(self) -> str:
        return self.f_name


if __name__ == '__main__':
    a1 = Robot('Falcon')
    print(a1, a1.objects_created)
    a2 = Robot('Eagle')
    print(a2, a2.objects_created)
    a3 = Robot('Night Wing')
    print(a3, a3.objects_created)
    a4 = Robot('Honey bee')
    print(a4, a4.objects_created)
    print(a1.objects_created)
    print(a2.objects_created)
    print(a3.objects_created)
    print(a4.objects_created)
    print(Robot.instances())
