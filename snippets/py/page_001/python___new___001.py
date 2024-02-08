from typing import Any, Self, Type


class Robot:
    __identity__: int = 0

    def __new__(cls: Type[Self], *args: Any, **kwargs: Any) -> Self:
        cls.__identity__ += 1
        return super().__new__(cls)

    def __init__(self, f_name: str = "Korangu") -> None:
        self.f_name = f_name
        pass

    @property
    def objects_created(self):
        return self.__identity__

    @classmethod
    def instances(cls):
        return cls.__identity__


if __name__ == "__main__":
    a1 = Robot("pa")
    print(a1, a1.objects_created)
    a2 = Robot("ka")
    print(a2, a2.objects_created)
    a3 = Robot("pi")
    a4 = Robot("ko")

    print(a3, a3.objects_created)
    print(a4, a4.objects_created)

    print()
    print(a1.objects_created)
    print(Robot.instances())
    pass
