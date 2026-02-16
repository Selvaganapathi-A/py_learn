from enum import IntEnum


class State(IntEnum):
    OFF = 0
    ON = 1
    UNDETERMINED = 2


def bulb(state: State) -> str:
    if state == State.ON:
        return "bulb is on."
    if state == State.OFF:
        return "bulb is off."
    raise NameError


def main():
    pass


if __name__ == "__main__":
    main()
