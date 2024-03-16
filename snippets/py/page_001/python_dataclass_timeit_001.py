import string
import timeit
from functools import partial
from secrets import choice
from typing import Final, Protocol, final

from dataclasses import dataclass, field

ASCII_CHARACTERS: Final[str] = (string.ascii_letters + string.ascii_lowercase +
                                string.ascii_uppercase)


class Staff(Protocol):

    def get_commision(self) -> tuple[int | float, str, bool]:
        ...


def generate_random_string_16(length: int = 16) -> str:
    return "".join((choice(ASCII_CHARACTERS) for _ in range(0, length)))


@final
@dataclass(
    order=True,
    # frozen=True,
    kw_only=True,
)
class Person:
    sort_index: int = field(
        init=False,
        repr=False,
    )
    name: str
    age: int
    student: str = "Yes"
    # email: list[str] = []
    email: list[str] = field(default_factory=list)
    id: str = field(
        init=False,
        default_factory=partial(
            generate_random_string_16,
            length=64,
        ),
    )
    _search_string: str = field(init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, "sort_index", self.age)
        object.__setattr__(self, "_search_string", self.name)

        # self.sort_index = self.age


@dataclass(
    order=True,
    # frozen=True,
    kw_only=True,
    slots=True,
)
class Person_Slots:
    sort_index: int = field(
        init=False,
        repr=False,
    )
    name: str
    age: int
    student: str = "Yes"
    # email: list[str] = []
    email: list[str] = field(default_factory=list)
    id: str = field(
        init=False,
        default_factory=generate_random_string_16,
    )
    _search_string: str = field(init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, "sort_index", self.age)
        object.__setattr__(self, "_search_string", self.name)

        # self.sort_index = self.age


def get_set_del(person: Person | Person_Slots):
    person.age = 90
    _ = person.age
    del person.age


def main():
    anita = Person(name="Anita", age=20)
    ws = min(timeit.repeat(partial(get_set_del, anita), number=1_000_000))

    anita = Person_Slots(name="Anita", age=20)
    s = min(timeit.repeat(partial(get_set_del, anita), number=1_000_000))

    print(((ws - s) / ws) * 100)
    print(s, ws)

    anita = Person(name="Anita", age=20)
    anita.email.append("anita+person@googlemail.com")

    michel = Person(name="Michel", age=18)
    michel.email.append("michel+person@googlemail.com")
    michel.email.append("michel+person_slot@live.com")

    rahul = Person(name="Rahul", age=21)
    rahul.email.append("rahul+person@googlemail.com")
    rahul.__setattr__("student", "No")
    print(rahul)
    print(anita, michel)
    print(anita > michel)


if __name__ == "__main__":
    main()
