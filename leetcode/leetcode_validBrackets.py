from learn.dsa.stack.stack import Stack


class Solution:
    def isValid(self, s: str) -> bool:
        stack = Stack[str]()
        for character in s:
            if character in "})]":
                if stack.isEmpty:
                    return False
                peek = stack.peek()
                if (character == ")" and peek != "(") or (character == "]" and peek != "["):
                    return False
                if character == "}" and peek != "{":
                    return False
                stack.pop()
            else:
                stack.insert(character)
        return stack.isEmpty


def main():
    s = "([{()}])[()]{[({{()}})]}"
    print(Solution().isValid(s))
    s = "))"
    print(Solution().isValid(s))
    s = "[)"
    print(Solution().isValid(s))


if __name__ == "__main__":
    main()
