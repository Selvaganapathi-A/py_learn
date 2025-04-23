from typing import Any, Callable


def debug(func_: Callable):

    def wrapper(*args, **kwargs):
        print(func_.__qualname__, 'is executing.')
        return func_(*args, **kwargs)

    return wrapper


class Fruit(type):

    def __new__(metaclass, name, bases, class_attrs, **kwargs):  # type:ignore
        class_ = type(metaclass.__name__, bases, class_attrs)
        for k, v in vars(class_).items():
            # print(k, v)
            if callable(v):
                setattr(class_, k, debug(v))
        for k, v in kwargs.items():
            setattr(class_, k, v)
        return class_


class Pine(metaclass=Fruit, k=0, m=8):
    id10t: int
    location: str = '+90.28424'

    def __str__(self):
        return self.__class__.__name__

    def add(self, other: Any):
        return other, id(other), hash(self)


if __name__ == '__main__':
    from subprocess import run

    run(('cls',), shell=True)
    p = Pine()
    print()
    print(p.__dict__)
    print()
    print(p.__annotations__)
    print()
    print()
    print(Pine.__dict__)
    print()
    print(Pine.__annotations__)
    print()
    print()
    print(p)
    print()
    print(p.add(9))
    print(p.add(78))
    print(p.add(89))
    print()
    print(p.k)
    print(p.m)
