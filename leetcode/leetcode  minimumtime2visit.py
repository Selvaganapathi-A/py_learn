from typing import List


import tracemalloc


class Solution:
    def minTimeToVisitAllPoints(self, points: List[List[int]]) -> int:
        distance = 0
        for i in range(1, len(points)):
            distance += max(
                abs(points[i - 1][0] - points[i][0]),
                abs(points[i - 1][1] - points[i][1]),
            )
        return distance


tracemalloc.start()
print(Solution().minTimeToVisitAllPoints([[1, 1], [3, 4], [-1, 0]]))
print(Solution().minTimeToVisitAllPoints([[3, 4], [-1, 2]]))
print("line 19", tracemalloc.get_traced_memory())
print(tracemalloc.get_tracemalloc_memory())
tracemalloc.stop()


def isPalindrome(x: int) -> bool:
    if x < 0:
        return False
    tmp = 0
    prev = x
    while True:
        tmp = (x % 10) + tmp * 10
        x = (x - (x % 10)) // 10
        if x == 0:
            break
    if prev == tmp:
        return True
    else:
        return False


print(isPalindrome(121))
