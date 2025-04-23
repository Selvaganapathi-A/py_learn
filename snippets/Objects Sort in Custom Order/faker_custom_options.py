from dataclasses import dataclass
from typing import Any, Literal, Union

from faker import Faker
from faker.providers import BaseProvider


class CustomProvider(BaseProvider):
    __provider__ = 'personalia'

    def __init__(self, generator: Any) -> None:
        self.__person_ages = tuple(range(16, 32))
        super().__init__(generator)

    def personalia(self):
        __person_gender = self.random_element(('F', 'M'))
        __person_name = (self.generator.name_male() if __person_gender == 'M'
                         else self.generator.name_female())
        __person_age = self.random_element(self.__person_ages)
        __person_email_address = f"{__person_name.lower().replace(' ', '_')} {2024 - __person_age}@{self.generator.domain_name()}"
        return Person(__person_name, __person_gender, __person_age,
                      __person_email_address)


@dataclass(slots=True, frozen=True)
class Person:
    name: str
    gender: Literal['M', 'F']
    age: float
    email: Union[str, None]


def main():
    faker = Faker()
    faker.add_provider(CustomProvider)
    # print(dir(faker))
    users: list[Person] = list()
    for _ in range(10):
        users.append(faker.personalia())
    print(users)


if __name__ == '__main__':
    main()
