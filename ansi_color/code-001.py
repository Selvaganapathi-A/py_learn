# from usha.stonk import a, b, c, d, e


def main():
    BLACK = '\033[0;30m'
    DARK_GRAY = '\033[1;30m'

    RED = '\033[0;31m'
    LIGHT_RED = '\033[1;31m'

    GREEN = '\033[0;32m'
    LIGHT_GREEN = '\033[1;32m'

    YELLOW = '\033[1;33m'
    LIGHT_YELLOW = '\033[1;93m'

    BLUE = '\033[0;34m'
    LIGHT_BLUE = '\033[1;34m'

    PURPLE = '\033[0;35m'
    LIGHT_PURPLE = '\033[0;95m'

    CYAN = '\033[0;36m'
    LIGHT_CYAN = '\033[1;36m'

    WHITE = '\033[0;37m'
    HEAVY_WHITE = '\033[1;37m'
    BOLD = '\033[1m'
    FAINT = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    DOUBLE_UNDERLINE = '\033[21m'
    BLINK = '\033[5m'
    NEGATIVE = '\033[7m'
    CROSSED = '\033[9m'
    END = '\033[0m'
    bg_colors = tuple(range(40, 48))
    print(bg_colors)

    bg_light_colors = tuple(range(100, 108))
    print(bg_light_colors)

    fg_colors = tuple(range(30, 38))
    print(fg_colors)

    fg_light_colors = tuple(range(90, 98))
    print(fg_light_colors)

    for x in range(30):
        print(f'\033[0;{x}m {x:_>4} \033[0m')
    print()
    for x in range(30, 38):
        print(f'\033[0;{x}m {x:_>4} \033[0m')
    print()
    for x in range(90, 98):
        print(f'\033[0;{x}m {x:_>4} \033[0m')
    print()
    for x in range(40, 48):
        print(f'\033[0;{x}m {x:_>4} \033[0m')
    print()
    for x in range(100, 108):
        print(f'\033[0;{x}m {x:_>4} \033[0m')
    print()

    print('\033[3m\033[97m\033[107m Hello Google \033[0m')
    text = '*** ███████████ ***'

    for x in range(256):
        print(f'\u001b[38;5;{x}m ░▒▓█▓▒░ \u001b[0m->{x:0>5x} {x:0>8b}')
    print()
    for x in range(256):
        print(f'\u001b[48;5;{x}m         \u001b[0m->{x:_>5x}')
    print()
    print(BOLD + text + END)
    print(ITALIC + text + END)
    print(UNDERLINE + text + END)
    print(DOUBLE_UNDERLINE + text + END)
    print(CROSSED + text + END)
    print()
    print(FAINT + LIGHT_PURPLE + text + END)
    print(PURPLE + text + END)
    print(LIGHT_PURPLE + text + END)
    print()
    print(CYAN + text + END)
    print(LIGHT_CYAN + text + END)
    print()
    print(BLACK + text + END)
    print(DARK_GRAY + text + END)
    print(WHITE + text + END)
    print(HEAVY_WHITE + text + END)
    print()


if __name__ == '__main__':
    main()
