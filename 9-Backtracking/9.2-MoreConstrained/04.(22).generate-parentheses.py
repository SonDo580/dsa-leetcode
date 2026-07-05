"""
https://leetcode.com/problems/generate-parentheses/

Given n pairs of parentheses,
write a function to generate all combinations of well-formed parentheses.

Well-formed parentheses definition:
- Every opening parenthesis must have a corresponding closing parenthesis.
- The parentheses are closed in correct order (the latest opened is closed first).
"""

"""
Idea:
- Use backtracking to generate all valid combinations. States needed:
  . curr: array of characters for current string being built
          (Don't use string since Python strings are immutable.
           A new string is created with every character added)
- Keep building a string by adding "(" or ")".
  . A "(" can be added at any point.
  . A ")" must match with a previous "(" 
    -> Only add a ")" if there are more "(" in the current string.
  . Previously added ")" should already satisfied this condition and have matching "(".
  . We can track number of "(" and ")" in stead of iterating through 'curr' to count every time .
    -> Extra states needed:
    . open_remains/close_remains: number of remaining "(" and ")" to use.
      (correspond to number of "(" and ")" in current string).
- Add the string to result after using all pairs.
"""


def generate_parentheses(n: int) -> list[str]:
    result: list[str] = []

    def backtrack(curr: list[str], open_remains: int, close_remains: int):
        if open_remains == 0:
            curr.extend([")"] * close_remains)  # add all remaining ")"
            result.append("".join(curr))
            for _ in range(close_remains):
                curr.pop()
            return

        # can always add "("
        curr.append("(")
        backtrack(curr, open_remains - 1, close_remains)
        curr.pop()

        # more remaining ")" than remaining "("
        # -> more "(" than ")" in current string
        # -> can add ")"
        if close_remains > open_remains:
            curr.append(")")
            backtrack(curr, open_remains, close_remains - 1)
            curr.pop()

    backtrack(curr=[], open_remains=n, close_remains=n)
    return result


"""
Complexity:

1. Time complexity:
- . (branching factor) At each step, we have at most 2 choices: add "(" or ")"
  . (recursion depth) Maximum length of the string: 2n
  -> work = total_nodes = O(2^(2n)) = O(4^n)
- . Build result string for each valid combination: O(2n) = O(n) 
  . num_valid_combinations < num_combinations = (2n)Cn
    (number of ways to choose n slots for n "(",
     the ")" will fit into remaining slots).
  -> work = O((2n)Cn)
=> Total work: O(4^n + (2n)Cn)

2. Space complexity: O(n)
- recursion stack: O(n)
- 'curr': O(n)
"""
