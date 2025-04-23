def some_function(a: int,
                  b: int,
                  /,
                  c: int,
                  d: int,
                  *,
                  e: int = 900,
                  f: int = 800):
    """Doc-String
    Example
        Non-Positional Arguments
        Positional Arguments
        Keyword Arguments
    """
    # ! Non Positional Arguments
    print(a)
    print(b)
    print()
    # ! Positional Arguments
    print(c)
    print(d)
    print()
    # ! Keyword Arguments
    print(e)
    print(f)


def main():
    some_function(6, 3, c=5, d=6)


if __name__ == '__main__':
    main()
