def robHouse(houses: list[int]) -> int:
    rob_1: int = 0
    rob_2: int = 0
    for house in houses:
        temp = max(house + rob_1, rob_2)
        rob_1 = rob_2
        rob_2 = temp
    return max(rob_1, rob_2)


def main():
    houses = [1, 2, 3, 1]
    result = robHouse(houses)
    print(result)
    houses = [1, 2, 3, 5, 2, 5, 6]
    result = robHouse(houses)
    print(result)
    pass


if __name__ == '__main__':
    main()
    pass
