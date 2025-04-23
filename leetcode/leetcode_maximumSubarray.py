def maximumSubArray(nums: list[int]) -> float:
    max_alltime = float('-inf')
    max_current = float('-inf')
    # i: int = 0
    # j: int = 0
    # k: int = 0
    for num in nums:
        # if max_alltime > max_current:
        #     j = max(i, j)
        # else:
        #     j += 1
        max_current = max(num, max_current + num)
        max_alltime = max(max_alltime, max_current)
        # print(f"{k:>2} {num:>3}, C={max_current:>3}, A={max_alltime:>3} ; j = ({i:>4}, {j:>4})")
        # if num > max_current + num:
        #     i += 1
        # k += 1

    return max_alltime


def main():
    nums: list[int]
    result: float
    #
    #
    #
    #
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4, -6]
    result = maximumSubArray(nums)
    print(result)
    #
    nums = [5, 4, -1, 7, 8]
    result = maximumSubArray(nums)
    print(result)
    pass


if __name__ == '__main__':
    main()
