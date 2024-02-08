from datetime import datetime
from typing import Any, Dict, NotRequired, Required, reveal_type, TypedDict
from typing import Unpack


class Movie(TypedDict):
    name: Required[str]
    released: NotRequired[datetime]


def func(**kwargs: Unpack[Movie]):
    release_date: datetime = kwargs.get("released", datetime(2060, 12, 31))
    print(kwargs["name"])
    print(release_date)
    print()
    print(kwargs)
    print()


def main():
    anabelle: Movie = {"name": "Anabelle"}
    func(**anabelle)
    #
    tin_tin: Dict[str, Any] = {
        "name": "Tin Tin's Adventures",
        "voice": "Ben Aflec",
    }
    func(**tin_tin)
    #
    a: float = 0.976
    print(reveal_type(a))


if __name__ == "__main__":
    main()
    pass
