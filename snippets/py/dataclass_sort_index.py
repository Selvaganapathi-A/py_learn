from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Literal, Self


@dataclass(eq=True)
class Person:
    name: str
    age: int
    gender: Literal['M', 'F', 'O']
    _sort_index: tuple[Literal['M', 'F', 'O'], int, str] = field(
        repr=False, init=False
    )

    def __post_init__(self: Self):
        self._sort_index = (self.gender, self.age, self.name)

    def __gt__(self: Self, other: Self):
        return self._sort_index > other._sort_index


def main():
    persons: Sequence[Person] = (
        Person('Iva Schneider', 26, 'F'),
        Person('Victor Norman', 23, 'M'),
        Person('Oscar Glover', 26, 'M'),
        Person('Adeline Flowers', 19, 'F'),
        Person('Winifred Cannon', 27, 'M'),
        Person('David Mendez', 19, 'M'),
        Person('Winnie Vargas', 16, 'F'),
        Person('Chad Fox', 26, 'M'),
        Person('Hulda Curry', 17, 'M'),
        Person('Harold Swanson', 17, 'M'),
        Person('Bernice McBride', 18, 'F'),
        Person('Brett Bradley', 17, 'M'),
        Person('Myrtle Bailey', 16, 'M'),
        Person('Patrick Curtis', 21, 'M'),
        Person('Lola Curtis', 26, 'F'),
        Person('Katherine Harper', 25, 'F'),
        Person('Vernon Pittman', 16, 'M'),
        Person('Lydia Dean', 23, 'F'),
        Person('Louise Ramos', 19, 'F'),
        Person('Hattie Harrison', 22, 'M'),
    )

    for person in sorted(persons):
        print(person)


if __name__ == '__main__':
    main()
