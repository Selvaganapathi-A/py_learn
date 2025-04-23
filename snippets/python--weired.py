# integer caching
#
# * less than 256 will be cached by default.
def main():
    a = int('234')
    b = int('234')
    print(a is b)  # ~ ok
    print()
    c = int('320')
    d = int('320')
    print(c is d)  # ~ Weired


if __name__ == '__main__':
    import os

    os.system('cls')
    main()
