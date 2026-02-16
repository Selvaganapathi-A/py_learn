def twoSum(nums: list[int], target: int) -> list[int]:
    window: dict[int, int] = dict()
    required: int = 0
    for i, num in enumerate(nums):
        required = target - num
        if num in window:
            return [window[num], i]
        window[required] = i
    return []


def main():
    nums: list[int] = [2, 7, 11, 15]
    target: int = 9
    result: list[int] = twoSum(nums, target)
    print(result)
    nums: list[int] = [3, 2, 4]
    target: int = 6
    result = twoSum(nums, target)
    print(result)
    nums: list[int] = [3, 3]
    target: int = 6
    result = twoSum(nums, target)
    print(result)


if __name__ == "__main__":
    main()
