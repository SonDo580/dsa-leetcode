# Given n pairs of parentheses,
# write a function to generate all combinations of well-formed parentheses.

# Example 1:
# Input: n = 3
# Output: ["((()))","(()())","(())()","()(())","()()()"]

# Example 2:
# Input: n = 1
# Output: ["()"]

# Constraints:
# 1 <= n <= 8


# ===== Definition =====
# Well-formed parentheses:
# - Every opening parenthesis must have a corresponding closing parenthesis.
# - The parentheses are closed in correct order (the lastest opened is closed first).

# ===== Analysis =====
# (*) Brute-force approach:
# - Generate all possible combinations:
#   + We can choose to use from 1 to n pairs -> the strings can have length from 2 to 2n.
#   + The number of strings with length 2m is the number of ways to choose m slots for the opening parentheses,
#     which is (2m)Cm (the closing parentheses must be placed in the remaining slots).
#   + Note: to avoid duplicates, only place later "(" after the slots for previous "(".
# - Check if the parentheses string is well-formed:
#   + Keep pushing characters onto a stack.
#   + If encounter a ")", and a "(" is on top of the stack, pop the "(" off the stack.
#   + If encounter a ")", the stack is empty, return False, since ")" must have corresponding "("
#   + After consume all characters, if the stack is empty, return True. Otherwise return False
#
# => Should use backtracking to stop exploring invalid path right away.

# ===== Observation =====
# - A "(" can be added at any point.
# - A ")" must match with a previous "(" -> only add a ")" if there are more "("s in the current string
#   + Previously added ")"s should already satisfy this condition and have matching "("s.
#     So we need at least 1 "(" in the current string to match with the new ")".
#   + We can compare numbers of remaining "("s and ")"s instead of looping through the current string.

# ===== Strategy =====
# - Use a function backtrack(current, open_remains, close_remains) to build the strings.
#   + current: the current string being built
#   + open_remains, close_remains: number of "("s and ")"s remaining.
# - Keep building a string by adding "(" or ")". Use the rules in <Observation>.
# - Add the string to result after using all "(" and ")". Then go back to explore the other paths.


def generate_parentheses(n: int) -> list[str]:
    result: list[str] = []

    def backtrack(current: str, open_remains: int, close_remains: int):
        if open_remains == 0:
            result.append(current + close_remains * ")")
            return

        backtrack(current + "(", open_remains - 1, close_remains)
        if close_remains > open_remains:
            backtrack(current + ")", open_remains, close_remains - 1)

    backtrack("", n, n)
    return result
