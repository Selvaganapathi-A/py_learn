from learn.dsa.stack.stack import Stack


class Solution:

    def isValid(self, s: str) -> bool:
        stack = Stack[str]()
        for character in s:
            if character in '})]':
                if stack.isEmpty:
                    return False
                else:
                    peek = stack.peek()
                    if character == ')' and peek != '(':
                        return False
                    elif character == ']' and peek != '[':
                        return False
                    elif character == '}' and peek != '{':
                        return False
                    else:
                        stack.pop()
            else:
                stack.insert(character)
        return stack.isEmpty


def main():
    s = '([{()}])[()]{[({{()}})]}'
    print(Solution().isValid(s))
    s = '))'
    print(Solution().isValid(s))
    s = '[)'
    print(Solution().isValid(s))
    pass


if __name__ == '__main__':
    main()
    pass
