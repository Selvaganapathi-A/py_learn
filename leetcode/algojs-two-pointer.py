import random


def order(numbers: list[int], number):
    left: int = 0
    right: int = 0
    switched: int = 0
    sequence_length = len(numbers)
    while right < sequence_length:
        if numbers[right] == number:
            numbers[left], numbers[right] = numbers[right], numbers[left]
            left = left + 1
            switched += 1
        right = right + 1
    return switched


def main():
    numbers: list[int] = [random.randint(0, 20) for _ in range(100)]
    print(numbers)
    print(order(numbers, 10))
    print(numbers)


if __name__ == '__main__':
    main()
