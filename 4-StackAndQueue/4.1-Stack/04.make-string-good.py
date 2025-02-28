# Given a string s of lower and upper case English letters.
# A good string is a string which doesn't have two adjacent characters s[i] and s[i + 1] where:
# . 0 <= i <= s.length - 2
# . s[i] is a lower-case letter and s[i + 1] is the same letter but in upper-case or vice-versa.
# To make the string good, you can choose two adjacent characters that make the string bad and remove them.
# You can keep doing this until the string becomes good.
# Return the string after making it good.
# The answer is guaranteed to be unique under the given constraints.
# Notice that an empty string is also good.

# Example 1:
# Input: s = "leEeetcode"
# Output: "leetcode"
# Explanation: In the first step, either you choose i = 1 or i = 2, both will result "leEeetcode" to be reduced to "leetcode".

# Example 2:
# Input: s = "abBAcC"
# Output: ""
# Explanation: We have many possible scenarios, and all lead to the same answer. For example:
# "abBAcC" --> "aAcC" --> "cC" --> ""
# "abBAcC" --> "abBA" --> "aA" --> ""

# Example 3:
# Input: s = "s"
# Output: "s"

# Constraints:
# 1 <= s.length <= 100
# s contains only lower and upper case English letters.

# ===== Strategy =====
# - We can use a stack and keep pushing characters in
# - When the new item and the latest item in the stack make the string bad,
#   pop the latest item from the stack and move to the next character
# - In the end, combine all the remaining characters in the stack

def make_string_good(s: str) -> str:
    # An empty string is a good string
    if len(s) == 0:
        return s

    stack: list[str] = []

    def is_bad(char: str):
        """
        Check if the current character and the last item on the stack
        make the string bad:
        - are the same character
        - 1 uppercase, 1 lowercase
        """
        return (
            char.lower() == stack[-1].lower() and 
            char.islower() != stack[-1].islower()
        )

    for char in s:
        if len(stack) == 0:
            stack.append(char)
            continue

        if is_bad(char):
            stack.pop()
        else:
            stack.append(char)

    return "".join(stack)

# ===== Complexity =====
#
# Time complexity:
# - iterate through all characters: O(n)
# - join the characters in the stack: O(n)
# => Overall: O(n)
#
# Space complexity: O(n)
# - space for the stack: O(n)