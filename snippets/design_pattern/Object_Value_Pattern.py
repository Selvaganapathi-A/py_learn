from typing import Self


class Price(float):
    def __new__(cls, value: float) -> Self:
        if value < 0:
            error_message = f"Price should'nt be zero. {value}"
            raise ValueError(error_message)
        return super().__new__(cls, value)


class Percentage(int):
    def __new__(cls, value: int) -> Self:
        minimum_percentage = 0
        maximum_percentage = 100

        if value < minimum_percentage or value > maximum_percentage:
            error_message = 'Percentage should be between zero and one hundred.'
            raise ValueError(error_message)

        return super().__new__(cls, value)


def calculate_discount(price: Price, percent: Percentage) -> float:
    return round(price * ((100 - percent) / 100), 2)


def main() -> None:
    print(calculate_discount(Price(1199), Percentage(1)))
    print(calculate_discount(Price(499), Percentage(0)))
    print(calculate_discount(Price(499), Percentage(1)))
    print(calculate_discount(Price(499), Percentage(25)))
    print(calculate_discount(Price(499), Percentage(50)))
    print(calculate_discount(Price(499), Percentage(100)))


if __name__ == '__main__':
    main()
