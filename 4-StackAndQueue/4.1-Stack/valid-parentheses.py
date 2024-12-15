# Given a string s containing just the characters
# '(', ')', '{', '}', '[' and ']',
# determine if the input string is valid.
#
# The string is valid if all open brackets are closed
# by the same type of closing bracket in the correct order,
# and each closing bracket closes exactly one open bracket.
#
# For example, s = "({})" and s = "(){}[]" are valid,
# but s = "(]" and s = "({)}" are not valid.


def is_valid_parens(s: str) -> bool:
    stack = []

    # use a dict to store closing brackets for opening brackets
    matching = {"(": ")", "[": "]", "{": "}"}

    for c in s:
        # c is an opening bracket -> add it to the stack
        if c in matching:
            stack.append(c)
            continue

        # c is a closing bracket

        # check if the stack is empty
        if len(stack) == 0:
            return False

        # check if c is the closing bracket for the latest opening bracket
        latest_opening_bracket = stack.pop()
        if matching[latest_opening_bracket] != c:
            return False

    # in the end, there should be no unmatched opening brackets
    return len(stack) == 0

# Analysis:
# - Time complexity: O(n)
#   (the stack's push and pop operations are (amortized) O(1))
# - Space complexity: O(n)