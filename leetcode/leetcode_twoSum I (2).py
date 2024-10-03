import os


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        temp: dict[int, int] = {}
        for i, num in enumerate(nums):
            need = target - num
            if need in temp:
                return [temp[need], i]
            else:
                temp[num] = i
        return []


def main():
    sol = Solution()
    #
    case_1 = [2, 7, 11, 15]
    print(sol.twoSum(case_1, 9))
    #
    case_2 = [3, 2, 4]
    print(sol.twoSum(case_2, 6))
    #
    case_3 = [3, 3]
    print(sol.twoSum(case_3, 6))
    #
    pass


if __name__ == "__main__":
    os.system("cls")
    main()
    pass
