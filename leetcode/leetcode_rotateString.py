import time
from collections.abc import Callable


def ti(fun: Callable[[str, str], bool]):
    def wra(s: str, goal: str):
        nonlocal fun
        st = time.perf_counter()
        res = fun(s, goal)
        ed = time.perf_counter()
        print(f'{(ed - st) * 1_000_000:9.3f} milliseconds')
        return res

    return wra


@ti
def rotateString(s: str, goal: str):
    if len(s) != len(goal):
        return False
    # return s in goal + goal
    goal += goal
    i: int = 0
    j: int = 0
    while j < len(goal):
        # print((i, j), (s[i], goal[j]))
        if s[i] == goal[j]:
            i += 1
            j += 1
            if i == len(s):
                return True
        else:
            if i > 0:
                j = j - i + 1
                i = 0
            else:
                j += 1
    return False


def main():
    s: str
    goal: str
    result: bool
    #
    s = 'abcde'
    goal = 'cdeab'
    result = rotateString(s, goal)
    print(result)
    #
    s = 'abcde'
    goal = 'abced'
    result = rotateString(s, goal)
    print(result)
    #
    s = 'bbbacddceeb'
    goal = 'ceebbbbacdd'
    result = rotateString(s, goal)
    print(result)


if __name__ == '__main__':
    main()
