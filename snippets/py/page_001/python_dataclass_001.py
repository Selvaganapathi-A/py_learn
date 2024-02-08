from dataclasses import dataclass
from datetime import datetime
from enum import auto, Enum

from dateutil.relativedelta import relativedelta


class EmploymentStatus(str, Enum):
    UNKNOWN = "Unknown"
    OTHER = "Other"
    STUDENT = "Studying"
    UNEMPLOYED = "Unemployed"
    SALARIED_WORK = "Salaried Person"
    FREELANCER = "Freelance Projects"
    OWN_BUSINESS = "Own Business"

    @classmethod
    def default(cls):
        return cls.UNKNOWN


class Gender(int, Enum):
    MALE = 1
    FEMALE = 2
    OTHER = auto()


@dataclass
class Person:
    first_name: str
    last_name: str
    gender: Gender
    date_of_birth: datetime
    employment_status: EmploymentStatus = EmploymentStatus.default()

    def about(self) -> str:
        age = relativedelta(datetime.now(), self.date_of_birth)
        return (
            f"{self.first_name.title()} {self.last_name.title()}"
            f" {self.gender.name} {age.years} years,"
            f" {age.months} months, {age.days} days old"
            f" {self.employment_status.value}."
        )


def main():
    sathya = Person(
        first_name="Sathya",
        last_name="Nathella",
        gender=Gender.FEMALE,
        date_of_birth=datetime(1995, 3, 18, 5, 40, 18),
        employment_status=EmploymentStatus.SALARIED_WORK,
    )
    print(sathya.about())
    print(Gender.OTHER)
    print(Gender.OTHER.name)
    print(Gender.OTHER.value)


if __name__ == "__main__":
    main()
