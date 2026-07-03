from secrets import choice

SPEED: tuple[int, ...] = tuple(range(1, 300, 1))


def speed():
    return choice(SPEED)


def alert():
    speed_ = speed()
    low_speed = 30
    medium_speed = 50
    high_speed = 75
    if speed_ < low_speed:
        return 'slow'
    if speed_ < medium_speed:
        return 'normal'
    if speed_ < high_speed:
        return 'high'
    return 'dangerous'


def main():
    pass


if __name__ == '__main__':
    main()
