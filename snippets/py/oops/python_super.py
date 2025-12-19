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
        return self.__dict__


if __name__ == '__main__':
    rectangle = Rectangle(80, 90)
    square = Square(70)
    print('Square Area', square.area())
    print('Square Perimeter', square.perimeter())
    print('Square View', square.view())

    print('Rectangle Area', rectangle.area())
    print('Rectangle Perimeter', rectangle.perimeter())
