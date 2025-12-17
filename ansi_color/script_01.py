def show_graphics(ansi_seq: str):
    iot: list[str] = []
    nos_per_line = 16
    for x in range(256):
        txt = f'{ansi_seq}{x}m{x:^3}\x1b[0m'
        if x % nos_per_line == 0:
            print('  '.join(iot))
            iot.clear()
        iot.append(txt)
    if iot:
        print(' '.join(iot))
    return


def main():
    nos_per_line = 16
    show_graphics('\x1b[38;5;')
    show_graphics('\x1b[48;5;')
    print()
    for x in range(256):
        if x % nos_per_line == 0:
            print()
            print()
        print(f'\x1b[{x}m' + f' {x:^3} ' + '\x1b[0m', end='')
    print()
    print()
    print('\x1b[48;5;14m' + '\x1b[38;5;255m' + 'Hello' + '\x1b[0m' + ' World.')
    print('\x1b[48;5;236m' + '\x1b[38;5;51m' + 'Hello' + '\x1b[0m' + ' World.')
    print(
        '\x1b[48;5;196m' + '\x1b[1;38;5;231m' + 'Hello' + '\x1b[0m' + ' World.'
    )
    print('\x1b[38;5;16m' + 'Hello' + '\x1b[0m' + ' World.')
    print('\x1b[38;5;232m' + 'Hello' + '\x1b[0m' + ' World.')


if __name__ == '__main__':
    main()
