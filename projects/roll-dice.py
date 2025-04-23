import logging
import secrets


def get_dice() -> int:
    return secrets.choice(seq=(1, 2, 3, 4, 5, 6))


def main():
    dice_count: int
    user_input: str

    try:
        user_input = input('Enter Number of Dice:')

        if user_input.lower() in ('exit', 'quit'):
            return

        dice_count: int = int(user_input)
        values = [get_dice() for _ in range(dice_count)]
        print(values, sum(values))

    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    main()
    pass
