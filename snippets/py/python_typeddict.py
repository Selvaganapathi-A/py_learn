from typing import TypedDict


class Person(TypedDict):
    first_name: str
    last_name: str


def get_people(name: str) -> Person:
    return {
        "first_name": name.split()[0],
        "last_name": name.split()[1],
    }


def main():
    print(get_people("meera ragavan"))
    print(get_people("dani jensen"))
    pass


if __name__ == "__main__":
    main()
