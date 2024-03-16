if __name__ == "__main__":
    lucifer: dict[str, int] = {"a": 5, "b": 7, "y": 4}
    chole: dict[str, int] = {"z": 5, "b": 2, "y": 6}
    #
    trixie: dict[str, int] = {
        k: lucifer.get(k, 0) + chole.get(k, 0) for k in set(chole | lucifer)
    }
    #
    print(lucifer)
    print(chole)
    print(trixie)
    #
