def Apple_init__(self, color):
    print("called init", self, color)
    self.color = color


def taste(self):
    return f"Apple Color : {self.color}"


Apple = type(
    "Apple",
    (),
    {
        "color": "red",
        "__init__": Apple_init__,
        "say": taste,
    },
)

apple: Apple = Apple("black")
print(Apple)
# print(dir(a))
print(apple.color)
print(apple.say())


if __name__ == "__main__":
    from subprocess import run

    run("cls", shell=True)

    class M:
        def __init__(self, n: float = 6) -> None:
            self.n = n
            self.__on_ = n

        def hello(self):
            return self.n

    a = M(89)

    print(M)
    print(dir(M))
    print()
    print(a)
    print(a.__setattr__("hello", 89))
    print(a)
    print(a.hello)
    print(a._M__on_)
    print()
