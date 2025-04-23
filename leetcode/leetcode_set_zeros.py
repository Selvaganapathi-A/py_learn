import secrets
import time
from subprocess import run
from typing import List

# from rich import print


class Solution:

    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        row_z: set[int] = set()
        col_z: set[int] = set()

        rows = len(matrix)
        if rows > 0:
            cols = len(matrix[0])
            #
            for x in range(rows):
                for y in range(cols):
                    if matrix[x][y] == 0:
                        col_z.add(y)
                        row_z.add(x)

            for x in row_z:
                for y in range(cols):
                    matrix[x][y] = 0
            for x in col_z:
                for y in range(rows):
                    matrix[y][x] = 0

        return matrix

    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        rs: int = 0
        re: int = len(matrix) - 1
        if re > 0:
            cs: int = 0
            ce: int = len(matrix[0]) - 1

            r, c = 0, 0

            while rs < re or cs < ce:
                print('---', (0, cs, ce), '---')
                print('---', (rs, 0, 0), '---')
                print('---', (re, 0, 0), '---')
                print()
                #

                print('fwd col')
                while cs <= c < ce:
                    # print(matrix[r][c])
                    print(((r, c), matrix[r][c]))
                    c += 1
                rs += 1
                time.sleep(1)
                print('---', (0, cs, c, ce), '---')
                print('---', (rs, 0, 0), '---')
                print('---', (r, 0, 0), '---')
                print('---', (re, 0, 0), '---')

                print('fwd row')
                while rs <= r < re:
                    # print(matrix[r][c])
                    print(((r, c), matrix[r][c]))
                    r += 1
                r -= 1
                ce -= 1
                time.sleep(1)
                print('---', (0, cs, ce), '---')
                print('---', (rs, 0, 0), '---')
                print('---', (re, 0, 0), '---')

                print('rev col')
                while cs <= c < ce:
                    # print(matrix[r][c])
                    print(((r, c), matrix[r][c]))
                    c -= 1
                c += 1
                re -= 1
                time.sleep(1)
                print('---', (0, cs, ce), '---')
                print('---', (rs, 0, 0), '---')
                print('---', (re, 0, 0), '---')

                print('rev row')
                while rs <= r < re:
                    # print(matrix[r][c])
                    print(((r, c), matrix[r][c]))
                    r -= 1
                r += 1
                cs += 1
                time.sleep(1)
                print('---', (0, cs, ce), '---')
                print('---', (rs, 0, 0), '---')
                print('---', (re, 0, 0), '---')
                print('-' * 40)

        time.sleep(5)

        return list()


def main():
    samples: list[list[list[int]]] = [
        [
            [1, 1, 2],
            [3, 5, 5],
            [0, 4, 1],
            [1, 3, 1],
            [3, 2, 5],
        ],
        [
            [2, 3, 4, 0, 4],
            [2, 4, 4, 2, 1],
            [2, 1, 4, 3, 1],
        ],
        [
            [3, 1, 5, 4, 3, 2, 2],
            [4, 4, 2, 5, 2, 3, 4],
            [4, 4, 1, 2, 5, 2, 1],
            [4, 4, 3, 2, 0, 0, 5],
            [3, 4, 2, 1, 0, 2, 5],
            [0, 5, 0, 1, 2, 1, 4],
        ],
        [
            [5, 0, 1, 4, 0, 1, 3],
            [0, 5, 4, 4, 3, 0, 0],
            [3, 2, 2, 0, 5, 3, 4],
        ],
        [
            [5, 1, 3],
            [1, 0, 2],
            [5, 3, 2],
        ],
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12],
        ],
    ]
    results = [
        [
            [1, 1, 2],
            [3, 5, 5],
            [0, 4, 1],
            [1, 3, 1],
            [3, 2, 5],
        ],
        [
            [2, 3, 4, 0, 4],
            [2, 4, 4, 2, 1],
            [2, 1, 4, 3, 1],
        ],
        [
            [0, 1, 0, 4, 0, 0, 2],
            [0, 4, 0, 5, 0, 0, 4],
            [0, 4, 0, 2, 0, 0, 1],
            [0, 4, 0, 2, 0, 0, 5],
            [0, 4, 0, 1, 0, 0, 5],
            [0, 5, 0, 1, 0, 0, 4],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [5, 0, 3],
            [0, 0, 0],
            [5, 0, 2],
        ],
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ],
    ]
    # value = tuple(x for x in range(0, 6))
    # for x in range(5):
    #     row = secrets.choice(range(3, 8))
    #     column = secrets.choice(range(3, 8))

    #     s1 = [list(secrets.choice(value) for x in range(row)) for y in range(column)]
    #     samples.append(s1)
    print(samples)

    for sample, result in zip(samples, results):
        print(sample)
        # print(Solution().setZeroes(sample) == result)
        print(Solution().spiralOrder(sample))
        # break
        print()
        print()
        print()
        print()

    pass


if __name__ == '__main__':
    run('clear')
    main()
    pass
