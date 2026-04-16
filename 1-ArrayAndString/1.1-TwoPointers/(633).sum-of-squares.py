"""
https://leetcode.com/problems/sum-of-square-numbers/

Given a non-negative integer c,
decide whether there're two integers a and b such that a^2 + b^2 = c.
"""

"""
Idea:
- Range of a & b:
  . Valid: -sqrt(c) -> sqrt(c)
  . We don't need to check negative numbers, since (-x)^2 = x^2 
    -> lower bound: 0
  . We only accept integers 
    -> upper bound: floor(sqrt(c))
- Strategy: use two pointers from both ends and move inwards
  . squares_sum == c -> found
  . squares_sum < c -> increase a
  . squares_sum > c -> decrease b
"""

import math


def judge_square_sum(c: int) -> bool:
    a = 0
    b = math.floor(math.sqrt(c))
    while a <= b:
        square_sum = a**2 + b**2
        if square_sum == c:
            return True
        elif square_sum < c:
            a += 1
        else:
            b -= 1
    return False


"""
Complexity:
1. Time complexity: O(sqrt(c))
2. Space complexity: O(1)
"""
