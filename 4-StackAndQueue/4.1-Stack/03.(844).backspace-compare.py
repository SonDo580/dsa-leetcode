"""
https://leetcode.com/problems/backspace-string-compare/

Given two strings s and t,
return true if they are equal when both are typed into empty text editors.
'#' means a backspace character.

For example, given s = "ab#c" and t = "ad#c", return true.
Because of the backspace, the strings are both equal to "ac"
"""

"""
Idea:
- Push normal characters to the stack.
- When backspace, pop the last item if the stack is not empty.
- Join the remaining characters in the end.
"""


def backspace_compare(s: str, t: str) -> bool:
    def get_final_string(string_with_backspaces: str) -> str:
        stack: list[str] = []

        for c in string_with_backspaces:
            if c != "#":
                # add normal characters to the stack
                stack.append(c)
            elif len(stack) > 0:
                # remove the latest typed character if c is a backspace
                stack.pop()

        return "".join(stack)

    return get_final_string(s) == get_final_string(t)

"""
Complexity:
- Let n = len(s)

1. Time complexity:
- iterate through s: O(n)
- join remaining characters: O(n)
=> Overall: O(n)

2. Space complexity: O(n) for the stack
"""