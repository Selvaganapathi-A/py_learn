import string


class Solution:

    def isPalindrome(self, s: str) -> tuple[bool, str]:
        l_ptr: int = 0
        r_ptr: int = len(s) - 1
        while l_ptr < r_ptr:
            print(s[l_ptr], s[r_ptr], l_ptr, r_ptr)
            if not s[l_ptr].isalnum():
                l_ptr += 1
            elif not s[r_ptr].isalnum():
                r_ptr -= 1
            elif s[l_ptr].lower() == s[r_ptr].lower():
                l_ptr += 1
                r_ptr -= 1
            else:
                return False, s
        return True, s


def main():
    s = 'A man, a plan, a canal: Panama '
    print(Solution().isPalindrome(s))
    s = 'aa'
    print(Solution().isPalindrome(s))
    s = '0P'
    print(Solution().isPalindrome(s))
    pass


if __name__ == '__main__':
    main()
    pass
