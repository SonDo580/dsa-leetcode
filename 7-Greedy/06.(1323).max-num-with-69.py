"""
https://leetcode.com/problems/maximum-69-number/

You are given a positive integer 'num' consisting only of digits 6 and 9.

Return the maximum number you can get by changing at most one digit
(6 becomes 9, and 9 becomes 6).
"""

"""
Strategy:
- To have the biggest number, flip the left-most 6.
- If there are no 6's, don't apply any changes.
"""


def max_num_from_69(num: int) -> int:
    return int(str(num).replace("6", "9", 1))


"""
Complexity:
- Let n = number of digits in 'num'

1. Time complexity:
- convert 'num' to string: O(n)
- replace the left most 6 with 9: O(n)
- convert num string back to integer: O(n)
=> Overall: O(n)

2. Space complexity:
- str(num) creates a new string: O(n)
- replace(...) creates another string: O(n)
=> Overall: O(n)
"""

# ===== Without string conversion (reduce extra space) =====
"""
- Find the leftmost 6's position (0-based, count from right).
- Flip that digit to 9 <-> increase num by (9-6)*10^i.
"""


def max_num_from_69(num: int) -> int:
    max_num = num
    position = 0
    position_to_flipped = -1

    while num > 0:
        digit = num % 10
        if digit == 6:
            position_to_flipped = position
        num //= 10
        position += 1

    if position_to_flipped != -1:
        max_num += 3 * 10**position_to_flipped

    return max_num


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
