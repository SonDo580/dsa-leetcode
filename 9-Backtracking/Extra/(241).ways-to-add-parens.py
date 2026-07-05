"""
https://leetcode.com/problems/different-ways-to-add-parentheses/

Given a string 'expression' of numbers and operators,
return all possible results from computing
all the different possible ways to group numbers and operators.
You may return the answer in any order.

The test cases are generated such that the output values fit in a 32-bit integer
and the number of different results does not exceed 104

Constraints:
. 'expression' consists of digits and the operator '+', '-', and '*'.
. The integer values in the input expression do not have a leading '-' or '+' denoting the sign.
. ...
"""

"""
Idea:
- Break the expressions into a list of tokens (operands and operators).
- Backtracking:
  . Iterate through the list and try to use each operator as the root.
    (Operator precedence doesn't matter since we can group arbitrarily).
  . Recurse on the left part to generate the list of first operands.
    Recurse on the right part to generate the list of second operands.
  . Compute results for all operand pairs.
  . Base case: If a part has only 1 token, it must be an operand.
- Optimize (becomes top-down DP):
  . The group range can overlap -> should cache results.
  . Example: 1 + 2 + 3 * 4 - 5
    . way 1: 1 + (2 + 3 * 4 - 5) = 1 + (2 + (3 * 4 - 5))
    . way 2: (1 + 2) + (3 * 4 - 5)
    -> both have to compute results for different groupings of (3 * 4 - 5)
"""

from typing import Callable
from functools import cache

# Handler for each operator
OPERATIONS: dict[str, Callable[[int, int], int]] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
}


def _tokenize(expression: str) -> list[str | int]:
    """
    Break expression into list of operands and operators.
    ('expression' consists of digits and the operator '+', '-', '*').
    """
    tokens: list[str | int] = []
    i = 0

    while i < len(expression):
        if expression[i] in OPERATIONS:
            # Collect operator
            tokens.append(expression[i])
            i += 1
            continue

        # Collect number operand
        start = i
        while i < len(expression) and expression[i].isdigit():
            i += 1
        tokens.append(int(expression[start:i]))

    return tokens


def _bin_op(op: str, a: int, b: int) -> int:
    """Return result of 'a op b'."""
    assert op in OPERATIONS
    return OPERATIONS[op](a, b)


def different_ways_to_compute(expression: str) -> list[int]:
    tokens = _tokenize(expression)

    @cache
    def _group(left: int, right: int) -> list[int]:
        """Compute results for all different grouping of tokens[left..right]."""
        if left == right:
            # 1 number operand
            assert isinstance(tokens[left], int)
            return [tokens[left]]

        results: list[int] = []
        for i in range(left, right + 1):
            if tokens[i] not in OPERATIONS:
                continue

            # Select current operator as root
            op = tokens[i]

            # Recursive to generate list of all operands
            a_list = _group(left, i - 1)
            b_list = _group(i + 1, right)

            # Try all operand pairs
            for a in a_list:
                for b in b_list:
                    results.append(_bin_op(op, a, b))

        return results

    return _group(left=0, right=len(tokens) - 1)


"""
Complexity: TODO
"""
