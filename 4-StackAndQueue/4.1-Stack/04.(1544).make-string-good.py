"""
https://leetcode.com/problems/make-the-string-great/

Given a string s of lower and upper case English letters.
A good string is a string which doesn't have two adjacent characters s[i] and s[i + 1] where:
. 0 <= i <= s.length - 2
. s[i] is a lower-case letter and s[i + 1] is the same letter but in upper-case or vice-versa.
To make the string good, you can choose 2 adjacent characters that make the string bad and remove them.
You can keep doing this until the string becomes good.
Return the string after making it good.
Notice that an empty string is also good.
"""

"""
Idea:
- Keep pushing characters to a stack.
- When the current item and the top of the stack make the string bad,
  pop the top of the stack.
- In the end, combine the remaining characters in the stack.
"""


def make_string_good(s: str) -> str:
    # An empty string is a good string
    if len(s) == 0:
        return s

    stack: list[str] = []

    def is_bad(char: str) -> bool:
        """
        Check if the current character and the top of the stack
        make the string bad:
        - are the same character.
        - 1 uppercase, 1 lowercase.
        """
        return (
            char.lower() == stack[-1].lower() and char.islower() != stack[-1].islower()
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


"""
Complexity:
- Let n = len(s)

1. Time complexity:
- iterate through s: O(n)
- join remaining characters: O(n)
=> Overall: O(n)

2. Space complexity: O(n) for the stack
"""
