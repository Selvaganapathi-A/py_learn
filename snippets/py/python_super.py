class Rectangle:
    def __init__(self, length: float, width: float):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)


class Square(Rectangle):
    def __init__(self, length: float):
        super(Square, self).__init__(length, length)

    def view(self):
        print(self.__dict__)


if __name__ == "__main__":
    rect = Rectangle(80, 90)

    sqr = Square(70)
    #
    print(sqr.area())
    print(sqr.perimeter())
    print(sqr.view())
    #
    print(rect.area())
    print(rect.perimeter())

    pass
