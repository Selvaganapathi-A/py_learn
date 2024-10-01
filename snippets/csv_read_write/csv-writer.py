from pathlib import Path
from typing import Literal

import csv
import dataclasses
import datetime
import os
import random

import faker
import faker_education


@dataclasses.dataclass(slots=True, frozen=True)
class Record:
    first_name: str
    last_name: str
    phone: str
    birth_day: datetime.date
    sex: Literal["M", "F", "O"]
    state: str
    zip_code: str

    def export(self):
        return (
            self.first_name,
            self.last_name,
            self.phone,
            self.birth_day,
            self.sex,
            self.state,
            self.zip_code,
        )


def funcname(fake: faker.Faker) -> Record:
    random_number: float = random.random()
    b_day: datetime.date = fake.date_between_dates(
        datetime.date(1990, 1, 1),
        datetime.date(2010, 12, 31),
    )
    state = fake.state()
    zip_code = fake.zipcode()
    phone = fake.phone_number()
    if random_number < 0.5:
        return Record(
            first_name=fake.first_name_female(),
            last_name=fake.last_name_female(),
            phone=phone,
            birth_day=b_day,
            sex="F",
            state=state,
            zip_code=zip_code,
        )

    return Record(
        first_name=fake.first_name_male(),
        last_name=fake.last_name_male(),
        phone=phone,
        birth_day=b_day,
        sex="M",
        state=state,
        zip_code=zip_code,
    )


def main():
    csv_file = Path(__file__).parent / "test_csv.csv"
    """
    newline = ""
    to avoid creating blank lines between rows
    """
    csv_file_descriptor = csv_file.open("w", newline='')
    csv_writer = csv.writer(
        csv_file_descriptor,
        delimiter=",",
    )

    fake: faker.Faker = faker.Faker("en-US")
    fake.add_provider(faker_education.SchoolProvider)
    #
    csv_writer.writerow((
        "First-Name",
        "Last-Name",
        "Phone-Number",
        "Birth-Day",
        "Sex",
        "State",
        "Zip-Code",
    ))

    for x in range(1000):
        csv_writer.writerow(funcname(fake).export())

    csv_file_descriptor.flush()
    csv_file_descriptor.close()

    pass


if __name__ == "__main__":
    os.system("cls")
    main()
    pass
