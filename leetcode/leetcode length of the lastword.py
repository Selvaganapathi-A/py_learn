## Length of Last Word
# Given a string s consisting of words and spaces, return the length of the last word in the string.
# A word is a maximal
# substring
#  consisting of non-space characters only.
# Example 1:
# Input: s = "Hello World"
# Output: 5
# Explanation: The last word is "World" with length 5.
# Example 2:
# Input: s = "   fly me   to   the moon  "
# Output: 4
# Explanation: The last word is "moon" with length 4.
# Example 3:
# Input: s = "luffy is still joyboy"
# Output: 6
# Explanation: The last word is "joyboy" with length 6.
# Constraints:
# 1 <= s.length <= 104
# s consists of only English letters and spaces ' '.
# There will be at least one word in s.
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        s: str = s[::-1]
        no_of_characters: int = 0
        found: bool = False
        for i in range(len(s)):
            if s[i] != ' ':
                no_of_characters += 1
                found = True
            elif found and s[i] == ' ':
                break
        return no_of_characters


print(Solution().lengthOfLastWord('   fly me   to   the moon  '))
