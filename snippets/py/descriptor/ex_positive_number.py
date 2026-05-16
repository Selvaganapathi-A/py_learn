from typing import Self


class PositiveNumber(int):
    def __set_name__(self, owner: type, name: str) -> None:
        print(owner.__name__, name)
        self.owner: type = owner
        self.field_name: str = name
        self._storage_name: str = f'_{name}'

    def __get__(self, instance: object | None, owner: type) -> Self | int:
        if instance is None:
            return self
        return instance.__dict__.get(self._storage_name, 0)

    def __set__(self, instance: object | None, value: int) -> None:
        if value < 0:
            raise ValueError
        instance.__dict__[self._storage_name] = value


class Basket:
    in_stock: PositiveNumber = PositiveNumber()

    def __init__(self, value: int) -> None:
        self.in_stock = value

    def sell(self, value: int) -> int:
        self.in_stock -= value
        return self.in_stock


if __name__ == '__main__':
    import logging
    import secrets
    import time

    logging.basicConfig(level=10, format='{asctime} - {message}', style='{')

    logger = logging.root

    apple_basket = Basket(100)
    number_sequence = tuple(range(1, 10))
    requested = secrets.choice(number_sequence)

    try:
        while True:
            available = apple_basket.sell(requested)
            logger.debug('Sold : %d | Available: %d', requested, available)
            requested = secrets.choice(number_sequence)
            time.sleep(0.2)

    except ValueError:
        logger.exception(  # noqa: LOG007
            'Requested Amount of apples is not Available. Requested : %d, Available : %s',
            requested,
            apple_basket.in_stock,
            exc_info=False,
        )
    print(apple_basket.in_stock)
