def high_common_factor(a: int, b: int, /):
    while b:
        a, b = b, a % b
    return a


def main():
    print(high_common_factor(40, 127688))


if __name__ == '__main__':
    main()
