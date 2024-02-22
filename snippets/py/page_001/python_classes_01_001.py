class Rectangle:

    def __init__(self, width: int, height: int):
        self.width, self.height = width, height

    def area(self):
        return self.width * self.height


class Square(Rectangle):

    def __init__(self, side: int) -> None:
        super(Square, self).__init__(side, side)


if __name__ == "__main__":
    square_plot = Square(5)
    rectangle_plot = Rectangle(3, 4)

    print("Area of Square    :", square_plot.area())
    print("Area of Rectangle :", rectangle_plot.area())
