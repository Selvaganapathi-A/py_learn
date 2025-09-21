from secrets import choice

SPEED: tuple[int, ...] = tuple(range(1, 300, 1))


def speed():
    return choice(SPEED)


def alert():
    speed_ = speed()

    if speed_ < 30:
        return 'slow'
    elif speed_ < 50:
        return 'normal'
    elif speed_ < 75:
        return 'high'
    else:
        return 'dangerous'


def main():
    print(alert())


if __name__ == '__main__':
    main()
