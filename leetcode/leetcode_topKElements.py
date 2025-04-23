from collections import defaultdict


def topKElements(nums: list[int], k: int) -> list[int]:
    # ! Leetcode Result
    orb: dict[int, int] = {}

    for i in nums:
        if i in orb:
            orb[i] += 1
        else:
            orb[i] = 1
    # print(sorted(orb, key=orb.get), orb)
    result: list[int] = []
    in_result = 0

    for x in sorted(orb.items(), key=lambda x: x[1], reverse=True):
        result.append(x[0])
        in_result += 1
        if in_result == k:
            return result
    return result


def main():
    nums: list[int]
    k: int
    result: list[int]
    #
    #
    #
    nums = [1, 1, 1, 2, 2, 3]
    k = 4
    result = topKElements(nums, k)
    print(result)
    #
    nums = [-1, 2, 0]
    k = 1
    result = topKElements(nums, k)
    print(result)
    #
    nums = [-2, -1, 2, 0, 8, 7, 4, 7, 1, 4, 7, 6, 4, 3]
    k = 3
    result = topKElements(nums, k)
    print(result)

    pass


def else_case(nums: list[int], k: int) -> list[int]:
    import heapq

    return heapq.nlargest(k, nums)


if __name__ == '__main__':
    main()
    pass
