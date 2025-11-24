from datetime import datetime
from typing import (Any, NotRequired, Required, TypedDict, Unpack,
                    reveal_type)


class Movie(TypedDict):
    name: Required[str]
    released: NotRequired[datetime]


def func(**kwargs: Unpack[Movie]):
    release_date: datetime = kwargs.get('released', datetime(2060, 12, 31))
    print(kwargs)
    print(kwargs['name'], release_date)
    print('-' * 80)


def main():
    anabelle: Movie = {'name': 'Anabelle'}
    func(**anabelle)
    tin_tin: dict[str, Any] = {
        'name': "Tin Tin's Adventures",
        'voice': 'Ben Aflec',
    }
    func(**tin_tin)
    a: float = 0.976
    print(reveal_type(a))


if __name__ == '__main__':
    main()
