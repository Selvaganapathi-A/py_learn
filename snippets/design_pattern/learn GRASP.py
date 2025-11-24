import datetime
from dataclasses import dataclass
from typing import Protocol


class CardInfo(Protocol):
    @property
    def number(self) -> str: ...
    @property
    def expiry_month(self) -> int: ...
    @property
    def expiry_year(self) -> int: ...


@dataclass(slots=True)
class DebitCard:
    number: str
    expiry_month: int
    expiry_year: int


@dataclass(slots=True)
class CreditCard:
    provider: str
    number: str
    expiry_month: int
    expiry_year: int


def luhn_checksum(number: str):
    # print(number)
    return sum((int(x) for x in number[-1::-2])) + sum((int(x) for x in number[-2::-2])) * 2


def validate_card(*, card: CardInfo):
    checksum = luhn_checksum(card.number)
    is_expired = datetime.datetime.now() < datetime.datetime(
        year=card.expiry_year, month=card.expiry_month, day=1
    )
    return checksum % 10 == 0 and is_expired


if __name__ == '__main__':
    print('Valid Card')
    card = DebitCard(r'1234567812345674', 10, 2025)
    print(card)
    if not validate_card(card=card):
        raise Exception('Card provided is not valid.', card)
    print('-' * 80)
    print('Invalid Card')
    card = CreditCard('JP Morgan', r'1234567812345674', 10, 2023)
    print(card)
    if not validate_card(card=card):
        raise Exception('Card provided is not valid.', card)
