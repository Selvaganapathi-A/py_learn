class Solution:
    def twoSum(self, numbers: list[int], target: int, /) -> list[int]:
        i: int = 0
        j: int = len(numbers) - 1
        result: int = 0
        while i < j:
            result = numbers[i] + numbers[j]
            if result == target:
                return [i + 1, j + 1]
            if result > target:
                j -= 1
            else:
                i += 1
        return []


def main():
    nums: list[int]
    target: int
    result: list[int]
    nums = [2, 7, 11, 15]
    target = 9
    result = Solution().twoSum(sorted(nums), target)
    print(result)
    nums = [2, 3, 4]
    target = 6
    result = Solution().twoSum(sorted(nums), target)
    print(result)
    nums = [-1, 0]
    target = -1
    result = Solution().twoSum(sorted(nums), target)
    print(result)
    nums = [-1, 0, 1, 1, 3, 5, 8]
    target = 2
    result = Solution().twoSum(sorted(nums), target)
    print(result)


if __name__ == '__main__':
    main()
