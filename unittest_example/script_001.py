from enum import IntEnum


class State(IntEnum):
    OFF = 0
    ON = 1
    UNDETERMINED = 2


def bulb(state: State) -> str:
    if state == State.ON:
        return "bulb is on."
    elif state == State.OFF:
        return "bulb is off."
    else:
        raise Exception


def main():
    on = State.ON
    print(bulb(on))
    off = State.OFF
    print(bulb(off))
    ud = State.UNDETERMINED
    print(bulb(ud))


if __name__ == "__main__":
    main()
    pass
