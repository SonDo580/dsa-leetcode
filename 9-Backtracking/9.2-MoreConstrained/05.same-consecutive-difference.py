# Given two integers n and k,
# return an array of all the integers of length n where the difference between every two consecutive digits is k.
# You may return the answer in any order.
# Note that the integers should not have leading zeros. Integers as 02 and 043 are not allowed.

# Example 1:
# Input: n = 3, k = 7
# Output: [181,292,707,818,929]
# Explanation: Note that 070 is not a valid number, because it has leading zeroes.

# Example 2:
# Input: n = 2, k = 1
# Output: [10,12,21,23,32,34,43,45,54,56,65,67,76,78,87,89,98]

# Constraints:
# 2 <= n <= 9
# 0 <= k <= 9


# ===== Analysis =====
# - For each number, we need to select n digits
#   Each slot has 10 options (0 -> 9),
#   The first slot has 9 options (1 -> 9)
# - The difference between consecutive digit is k
#   -> After selecting digit x, try 2 digits x - k and x + k
#      for the next digit (make sure to stay in bound)

# ===== Strategy =====
# - Use a recursive function backtrack(num, last_digit, num_length)
#   . num: the number being built
#   . last_digit: the last digit of 'num'
#   . num_length: the length of 'num'
# - A valid answer is found after we select n digits.
# - Note: last_digit and num_length can be deduced from 'num',
#         but I included them to reduce computation.
# - Special case: if k = 0, just generate use the same digit for n slots.


def numbers_with_same_consecutive_difference(n: int, k: int) -> list[int]:
    result: list[int] = []

    def backtrack(num: int, last_digit: int, num_length: int):
        if num_length == n:
            result.append(num)
            return

        for next_digit in [last_digit - k, last_digit + k]:
            if 0 <= next_digit <= 9:
                backtrack(num * 10 + next_digit, next_digit, num_length + 1)

    def num_from_1_digit(digit: int, length: int) -> int:
        """Generate a number of specified length from 1 digit"""
        num = 0
        for _ in range(length):
            num = num * 10 + digit
        return num

    for digit in range(1, 10):
        if k == 0:
            result.append(num_from_1_digit(digit, length=n))
        else:
            backtrack(num=digit, last_digit=digit, num_length=1)

    return result
