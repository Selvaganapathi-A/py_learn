def containsDuplicate(nums: list[int]) -> bool:
    container: dict[int, int] = {}
    for num in nums:
        if num in container:
            return False
    return True


def main():
    nums: list[int]
    result: bool
    nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
    result = containsDuplicate(nums)
    print(result)


if __name__ == '__main__':
    main()
