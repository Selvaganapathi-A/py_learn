import collections


class Solution:
    def slidingWindowMaximumMonotonicQueue(
        self, nums: list[int], k: int
    ) -> list[int]:
        # *  list to store the maximum values for each sliding window
        result = []
        # *  Deque to store indices of elements in the current window
        double_ended_queue = collections.deque()
        # *  Pointers for the sliding window
        left_pointer = right_pointer = 0
        while right_pointer < len(nums):
            # *  Pop smaller values from the back of the deque
            while (
                len(double_ended_queue) > 0
                and nums[double_ended_queue[-1]] < nums[right_pointer]
            ):
                double_ended_queue.pop()
            # * add right pointer
            double_ended_queue.append(right_pointer)
            # *  Remove the leftmost value if it's outside the current window
            if left_pointer > double_ended_queue[0]:
                double_ended_queue.popleft()
            # *  If the window size is reached, append the maximum value to the result
            if (right_pointer + 1) >= k:
                result.append(nums[double_ended_queue[0]])
                left_pointer += 1
            right_pointer += 1
        return result


def main():
    samples = [
        [
            3,
            [-3, 38, 30, -36, 30, -35, 20, -8],
        ],
        [
            4,
            [42, 8, -18, -33, 11, 45, 4, 32, -22],
        ],
        [
            5,
            [-15, 38, -46, -17, 26, 47, 1, 10, 3, -10, -2, -38],
        ],
        [
            6,
            [
                46,
                -47,
                30,
                -1,
                37,
                -3,
                46,
                9,
                -38,
                -12,
                26,
                4,
                33,
                46,
                -16,
                -28,
                2,
                7,
                -26,
                -21,
                -30,
                -47,
                22,
                34,
                -31,
                -36,
                -15,
                -49,
                30,
                25,
                -31,
            ],
        ],
        [
            7,
            [
                23,
                5,
                50,
                -21,
                -36,
                -34,
                15,
                -17,
                6,
                24,
                -15,
                -21,
                -39,
                -41,
                -29,
                30,
                21,
                -38,
                38,
                9,
                8,
                16,
                31,
                6,
                -47,
                -14,
                16,
                -49,
                -6,
                2,
                8,
                -10,
                -30,
                14,
                35,
                10,
                3,
                39,
                -8,
            ],
        ],
        [
            8,
            [
                -14,
                36,
                45,
                36,
                -25,
                -5,
                -47,
                23,
                46,
                39,
                35,
                32,
                -23,
                37,
                14,
                14,
                21,
                1,
                -13,
                -43,
                -50,
                39,
                26,
                -49,
                -13,
                31,
                -15,
                -13,
                -29,
                -32,
                29,
                26,
                34,
                -24,
                20,
                -41,
                -50,
                1,
                48,
                -29,
            ],
        ],
    ]
    nums: list[int]
    k: int
    result: list[int]
    solution = Solution()
    for k, nums in samples:
        print('k = ', k)
        print('nums = ', nums)
        result = solution.slidingWindowMaximumMonotonicQueue(nums, k)
        print(result)


if __name__ == '__main__':
    import os

    os.system('clear')
    main()
