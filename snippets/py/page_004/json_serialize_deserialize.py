import json
from decimal import Decimal
from typing import Any


class Apple:

    def __init__(self, place: str, price: Decimal) -> None:
        self.place: str = place
        self.price: Decimal = price

    def __repr__(self) -> str:
        return f'Apple(place="{self.place}", price="{self.price}")'


def serializer(value: Any):
    if isinstance(value, Decimal):
        return {'type': 'decimal', 'value': str(value)}
    elif isinstance(value, Apple):
        return {
            'type': 'Apple',
            'attrs': {
                'place': value.place,
                'price': value.price,
            },
        }
    raise TypeError


def deserialize(value: Any):
    match value:
        case {'type': 'decimal', 'value': str()}:
            return Decimal(value['value'])
        case {
            'type': 'Apple',
            'attrs': {
                'place': str(),
                'price': Decimal(),
            },
        }:
            return Apple(
                place=value['attrs']['place'],
                price=value['attrs']['price'],
            )
        case _:
            return value


def main():
    a = Apple('ohio', Decimal('12.49'))
    b = Apple('yorktown', Decimal('14.99'))
    c = {'ohio apples': a, 'yorktown apples': {'newyork apples': b}}
    x1 = json.dumps(c, default=serializer)
    print(x1)
    print()
    print()
    print()
    x2 = json.loads(x1, object_hook=deserialize)
    print(x2)
    ak: Apple = x2['ohio apples']
    print(ak.place)
    print(round(ak.price, 4))


if __name__ == '__main__':
    main()
