def main():
    x: int
    for x in range(256):
        txt = f'\x1b[38;5;{x}m{x: ^4}\x1b[0m'
        print(txt, flush=True, end=' ')
        if x % 16 == 15:
            print()
    print('\n' * 4)
    for x in range(256):
        txt = f'\x1b[48;5;{x}m{x: ^4}\x1b[0m'
        print(txt, flush=True, end=' ')
        if x % 16 == 15:
            print()
    print()


if __name__ == '__main__':
    main()
