class Fruit:

    def is_organic(self):
        raise NotImplementedError(
            'Method Not Implemented.'
        )    # indicates this method, should be implemented in subclasses.


class Apple(Fruit):

    def __init__(self, price: float) -> None:
        self.price: float = price

    def __eq__(self, value: object) -> bool:
        # print('equals', self, value)
        if not isinstance(value, Apple):
            return NotImplemented
        return self.price == value.price

    def __ne__(self, value: object) -> bool:
        # print('not equals', self, value)
        if not isinstance(value, Apple):
            return NotImplemented    # return NotImplemented. fallbacks to pythons default comparison.
        return self.price != value.price

    def __repr__(self) -> str:
        return f"Apple(price={self.price})"


def main():
    a = Apple(34.55)
    b = Apple(34.55)
    #
    print(a.is_organic())
    print(a == b)
    print(a == 33.34)
    print()
    #
    print(a != 33.34)
    print(a != b)
    pass


if __name__ == "__main__":
    main()
    pass
