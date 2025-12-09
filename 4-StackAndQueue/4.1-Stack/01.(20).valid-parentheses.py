"""
https://leetcode.com/problems/valid-parentheses/

Given a string s containing just the characters
'(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

The string is valid if all open brackets are closed
by the same type of closing bracket in the correct order,
and each closing bracket closes exactly one open bracket.

For example, s = "({})" and s = "(){}[]" are valid,
but s = "(]" and s = "({)}" are not valid.
"""

"""
Idea:
- Keep pushing opening brackets to a stack. 
- When we encounter a closing bracket, it should correspond to 
  the most recent opening bracket.
  . If they match, pop the opening bracket off the stack.
  . If they don't match, or there's no opening brackets to pair with
    (empty stack), s is invalid.
- After consuming all characters in s, the stack should be empty.
  If there are opening brackets remain, s is invalid. 
"""

def is_valid_parens(s: str) -> bool:
    stack: list[str] = []

    # Store closing brackets for opening brackets
    matching = {"(": ")", "[": "]", "{": "}"}

    for c in s:
        # c is an opening bracket -> add it to the stack
        if c in matching:
            stack.append(c)
            continue

        # c is a closing bracket

        # The stack is empty -> no opening bracket to match with
        if len(stack) == 0:
            return False

        # Check if c is the closing bracket for the latest opening bracket
        latest_opening_bracket = stack.pop()
        if matching[latest_opening_bracket] != c:
            return False

    # In the end, there should be no unmatched opening brackets
    return len(stack) == 0

"""
Complexity:
- Let n = len(s)

1. Time complexity: O(n)
2. Space complexity: O(n) for the stack
"""