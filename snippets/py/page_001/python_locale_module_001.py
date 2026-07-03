import locale


def main():
    locale.setlocale(locale.LC_ALL, 'en_IN')
    principle: int = 4_00_00_000
    print(locale.currency(principle, grouping=True))
    print(locale.currency(principle, grouping=True, international=True))


if __name__ == '__main__':
    main()
