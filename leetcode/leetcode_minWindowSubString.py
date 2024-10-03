from subprocess import run


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        length_s: int = len(s)
        length_t: int = len(t)
        if t == "" or length_t > length_s:
            return ""
        result: list[int] = [-1, -1]
        result_length: float = float("inf")
        count_in_t: dict[str, int] = {}
        window: dict[str, int] = {}
        for c in t:
            count_in_t[c] = count_in_t.get(c, 0) + 1
        character: str = ""
        have: int = 0
        need: int = len(count_in_t)
        left_pointer: int = 0
        current_pointer: int = 0
        for current_pointer in range(length_s):
            character = s[current_pointer]
            window[character] = window.get(character, 0) + 1
            if character in count_in_t and window[character] == count_in_t[character]:
                have += 1
            while have == need:
                if (current_pointer - left_pointer + 1) < result_length:
                    result = [left_pointer, current_pointer]
                    result_length = current_pointer - left_pointer + 1
                window[s[left_pointer]] -= 1
                if (
                    s[left_pointer] in count_in_t
                    and window[s[left_pointer]] < count_in_t[s[left_pointer]]
                ):
                    have -= 1
                left_pointer += 1
        left_pointer, current_pointer = result
        final_result: str = (
            s[left_pointer : current_pointer + 1] if result_length != float("inf") else ""
        )
        return final_result


def main():
    solution = Solution()
    #
    s: str = "ADOBECODEBANC"
    t: str = "ABC"
    result = solution.minWindow(s, t)
    print(result)
    #
    s = "a"
    t = "a"
    result = solution.minWindow(s, t)
    print(result)
    #
    s = "a"
    t = "aa"
    result = solution.minWindow(s, t)
    print(result)
    #
    s = "selvaganapathi"
    t = "lvn"
    result = solution.minWindow(s, t)
    print(result)
    #
    pass


if __name__ == "__main__":
    run(
        "clear",
    )
    main()

    pass
