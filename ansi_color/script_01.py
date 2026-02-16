def show_graphics(ansi_seq: str, nos_per_line: int = 10):
    iot: list[str] = []
    for x in range(256):
        txt = f"{ansi_seq}{x}m{x:^3}\x1b[0m"
        if x % nos_per_line == (nos_per_line - 1):
            print("  ".join(iot))
            iot.clear()
        iot.append(txt)
    if iot:
        print(" ".join(iot))


def main():
    import shutil

    cols, rows = shutil.get_terminal_size()

    nos_per_line = 16
    for x in range(1, 16):
        new_col = x**2
        print(new_col, cols)
        if cols < new_col:
            nos_per_line = x - 1
            break
    print(nos_per_line)

    show_graphics("\x1b[38;5;")
    show_graphics("\x1b[48;5;")
    print()
    for x in range(256):
        if x % nos_per_line == (nos_per_line - 1):
            print()
            print()
        print(f"\x1b[{x}m" + f" {x:^3} " + "\x1b[0m", end="")


if __name__ == "__main__":
    main()
