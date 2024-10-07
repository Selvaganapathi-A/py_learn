from script_01 import Range


def main():
    print("stop")
    for x in Range[int](10):
        print(x)
    print("start stop")
    for x in Range[float](0.25, 10, 2.25):
        print(x)
    print("start stop step")
    for x in Range[int](0, 17, 4):
        print(x)
    print()


if __name__ == "__main__":
    main()
    pass
