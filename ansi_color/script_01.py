def show_graphics(ansi_seq: str):
    iot: list[str] = list()
    #
    nos_per_line = 16
    #
    for x in range(256):
        txt = ansi_seq + f"{x}m" + f"226{x:^3}" + "\x1B[0m"
        if x % nos_per_line == 0:
            print(" ".join(iot))
            iot.clear()
        iot.append(txt)
    #
    if iot:
        print(" ".join(iot))
    #
    return


def main():
    show_graphics("\x1B[38;5;")
    show_graphics("\x1B[48;5;")

    print()
    print()
    print()
    for x in range(258):
        print(f"\x1B[{x}m" + f" {x:^3} " + "\x1B[0m", end=", ")
    print()
    print()
    print()
    print("\x1B[48;5;14m" + "\x1B[38;5;255m" + "Hello" + "\x1B[0m" + " World.")
    print("\x1B[48;5;236m" + "\x1B[38;5;51m" + "Hello" + "\x1B[0m" + " World.")
    print("\x1B[48;5;196m" + "\x1B[1;38;5;231m" + "Hello" + "\x1B[0m" +
          " World.")
    print("\x1B[38;5;16m" + "Hello" + "\x1B[0m" + " World.")
    print("\x1B[38;5;232m" + "Hello" + "\x1B[0m" + " World.")
    pass


if __name__ == "__main__":
    main()
    pass
