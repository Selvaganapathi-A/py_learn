import json5


class Serializer:

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        pass

    def serialize(self):
        return self.kwargs


class Rectangle(Serializer):

    def __init__(self, width=50, height=100, *args) -> None:
        super().__init__(width=width, height=height)


class Square(Serializer):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Circle(Serializer):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class House(Serializer):

    def __init__(
        self, rectangle: Rectangle, square: Square, circle: Circle
    ) -> None:
        self.rectangle = rectangle
        self.square = square
        self.circle = circle

    def serialize(self) -> dict[str, dict[str, int]]:
        # print(self.floor.__dict__)
        return {
            "rectangle": self.rectangle.serialize(),
            "square": self.square.serialize(),
            "circle": self.circle.serialize(),
        }


if __name__ == "__main__":
    h = House(
        Rectangle(width=50, height=100),
        Square(sides=45),
        Circle(radius=20),
    )
    print(json5.dumps(h.serialize(), sort_keys=True))
    print(json5.dumps(h.serialize()))

    pass
