class Solution:

    def productOfArrayExceptSelf(self, nums: list[int]) -> list[int]:
        # n, ans, suffix_prod = len(nums), [1] * len(nums), 1

        # for i in range(1, n):
        #     ans[i] = ans[i - 1] * nums[i - 1]

        # for i in range(n - 1, -1, -1):
        #     ans[i] *= suffix_prod
        #     suffix_prod *= nums[i]

        # return ans
        ln = len(nums)
        i: int = 1
        j: int = ln - 1
        temp: int = 1
        result: list[int] = [1] * ln
        while i < ln:
            result[i] = result[i - 1] * nums[i - 1]
            i += 1
        while j >= 0:
            result[j] = result[j] * temp
            temp = temp * nums[j]
            j -= 1
        return result


def main():
    arr = [2, 3, 4, 3, 2]
    print(Solution().productOfArrayExceptSelf(arr))
    pass


if __name__ == '__main__':
    main()
    pass
