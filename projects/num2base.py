import string

_TEXT = string.digits + string.ascii_uppercase + string.ascii_lowercase + '#$'
_TEXT_LENGTH = len(_TEXT)
#
MAPPED_TO_CHARACTER = {x: _TEXT[x] for x in range(_TEXT_LENGTH)}
MAPPED_TO_NUMBER = {_TEXT[x]: x for x in range(_TEXT_LENGTH)}


def numberToBase(number: int, base: int) -> str:
    if number == 0:
        return '0'
    digits: list[int] = []
    while number:
        reminder = number % base
        number = number - reminder
        number //= base
        digits.append(reminder)
    return ''.join(MAPPED_TO_CHARACTER[x] for x in digits[::-1]) + f' {base}'


def main():
    number: int = 127
    base = len(_TEXT)
    print()
    print(MAPPED_TO_CHARACTER)
    # print(MAPPED_TO_NUMBER)
    print()
    print(numberToBase(number, base))


if __name__ == '__main__':
    import os

    os.system('clear')
    main()
