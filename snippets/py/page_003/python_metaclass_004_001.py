class Fruit(type):
    handlers: dict = {}

    def __new__(cls, name, bases, attrs, **optional_dict):
        # cls_ = super().__new__(metaclass_, name, bases, attrs)
        cls_ = type(name, bases, attrs)
        if cls_.__name__ not in cls.handlers:
            cls.handlers[cls_.__name__] = cls_
        else:
            raise ValueError(cls_.__name__, 'Created Already.')
        for k, v in optional_dict.items():
            setattr(cls_, k, v)
        return cls_


class Apple(metaclass=Fruit, origin='india', color='red'):
    origin: str
    color: str

    def __init__(self, origin: str, color: str) -> None:
        self.origin = origin
        self.color = color


class Orange(metaclass=Fruit): ...


class Banana(metaclass=Fruit): ...


class Guaua(metaclass=Fruit): ...


class PineApple(metaclass=Fruit): ...


class StrawBerry(metaclass=Fruit): ...


class BlueBerry(metaclass=Fruit):
    def __new__(cls):
        print('Hi')
        return object.__new__(cls)


if __name__ == '__main__':
    from subprocess import run

    run(
        ('cls',),
        shell=True,
    )
    a = Apple('iran', 'black')
    print(a.origin)
    print(a.color)
    print(Apple.origin)
    print(Apple.color)
    print(type(a))
    print(type(Apple))
    print(Fruit.handlers)
    print('-' * 80)
    bb = BlueBerry()
    print(bb)
    print(type(bb))
    print('-' * 80)
