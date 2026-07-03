import warnings


def somefn():
    warnings.warn('function will be removed after major version change.', FutureWarning)


def main():
    with warnings.catch_warnings(record=True) as w:
        somefn()
        print(w[0].message)
        print(w[0].category)
        print(w[0].source)

    somefn()
    somefn()
    somefn()
    somefn()


if __name__ == '__main__':
    main()
