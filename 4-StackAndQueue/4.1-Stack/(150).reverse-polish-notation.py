"""
https://leetcode.com/problems/evaluate-reverse-polish-notation/

You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.
Evaluate the expression. Return an integer that represents the value of the expression.

Note that:
- The valid operators are '+', '-', '*', and '/'.
- Each operand may be an integer or another expression.
- The division between two integers always truncates toward zero.
- There will not be any division by zero.
- The input represents a valid arithmetic expression in a reverse polish notation.
- The answer and all the intermediate calculations can be represented in a 32-bit integer.

Reverse Polish Notation:
- a mathematical notation in which operators follow their operands.
- example: 3 4 + (add 3 and 4)
"""

"""
Idea:
- Keep pushing number tokens to a stack
- When encounter an operator, pop 2 numbers off the stack,
  perform the operation, and push the result back.
- Repeat until all tokens are consumed.
  Return the last remaining value on the stack.
"""

from typing import Callable


def eval_RPN(tokens: list[str]) -> int:
    OPERATIONS: dict[str, Callable[[int, int], int]] = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b),  # truncate toward 0
    }

    stack: list[int] = []

    for token in tokens:
        if token in OPERATIONS:
            # token is an operator
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = OPERATIONS[token](operand1, operand2)
            stack.append(result)
        else:
            # token is a number
            stack.append(int(token))

    return stack.pop()


print(eval_RPN(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]))


"""
Complexity:
- Let n = len(tokens)

1. Time complexity: O(n)
- each number token is added and removed once.
- the number of intermediate results = the number of operator tokens
  (compute and push back)

2. Space Complexity: O(n) for the stack
"""
