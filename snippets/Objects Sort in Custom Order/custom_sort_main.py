from typing import Literal

from custom_sort_data import Person, users


def get_name(person: Person) -> str:
    """
    Description:
        Returns the name of the given person.
    Parameters:
        person: An instance of the Person class representing a person.
    Returns:
        str: The name of the person.
    """
    return person.name


def get_age(person: Person) -> float:
    """
    Description:
        Returns the age of the given person.
    Parameters:
        person: An instance of the Person class representing a person.
    Returns:
        float: The age of the person.
    """
    return person.age


def get_gender_age_name(person: Person) -> tuple[Literal["M", "F"], float, str]:
    """
    Description:
        Returns a tuple containing the gender, age, and name of the given person.
    Parameters:
        person: An instance of the Person class representing a person.
    Returns:
        tuple: A tuple containing the gender, age, and name of the person.
            Literal['M', 'F']: The gender of the person, either 'M' for male or 'F' for female.
            float: The age of the person.
            str: The name of the person.
    """
    return person.gender, person.age, person.name


def main():
    """
    Description: Executes sorting operations on the users data.
    """
    # * Sort by Name
    print("\x1b[48;5;196m\x1b[38;5;15m                                      \x1b[0m")
    print("\x1b[48;5;196m\x1b[38;5;15m        Sort by Name                  \x1b[0m")
    print("\x1b[48;5;196m\x1b[38;5;15m                                      \x1b[0m")
    for person in sorted(users, key=get_name):
        print(person)
    print("-" * 80)
    print()
    # * Sort by Age
    print("\x1b[48;5;196m\x1b[38;5;15m                                      \x1b[0m")
    print("\x1b[48;5;196m\x1b[38;5;15m        Sort by Age                   \x1b[0m")
    print("\x1b[48;5;196m\x1b[38;5;15m                                      \x1b[0m")
    for person in sorted(users, key=get_age):
        print(person)
    print("-" * 80)
    # * Sort by gender, age then name
    print("\x1b[48;5;196m\x1b[38;5;15m                                      \x1b[0m")
    print("\x1b[48;5;196m\x1b[38;5;15m    Sort by Gender, Age then Name     \x1b[0m")
    print("\x1b[48;5;196m\x1b[38;5;15m                                      \x1b[0m")
    for person in sorted(users, key=get_gender_age_name):
        print(person)
    print("-" * 80)
    print()


if __name__ == "__main__":
    main()
