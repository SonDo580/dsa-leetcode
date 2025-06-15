# You are given a positive integer num consisting only of digits 6 and 9.

# Return the maximum number you can get by changing at most one digit
# (6 becomes 9, and 9 becomes 6).


# Example 1:
# Input: num = 9669
# Output: 9969
# Explanation:
# Changing the first digit results in 6669.
# Changing the second digit results in 9969.
# Changing the third digit results in 9699.
# Changing the fourth digit results in 9666.
# The maximum number is 9969.

# Example 2:
# Input: num = 9996
# Output: 9999
# Explanation: Changing the last digit 6 to 9 results in the maximum number.

# Example 3:
# Input: num = 9999
# Output: 9999
# Explanation: It is better not to apply any change.


# Constraints:
# 1 <= num <= 10^4
# num consists of only 6 and 9 digits.


# ===== Observation =====
# - To have the biggest number, flip the left-most 6.
# - If there are no 6's, don't apply any changes.


def max_num_from_69(num: int) -> int:
    return int(str(num).replace("6", "9", 1))


# ===== Complexity =====
# Let n = number of digits
#
# 1. Time complexity:
# - convert num to string: O(n)
# - replace the left most 6 with 9: O(n)
# - convert num string back to integer: O(n)
# => Overall: O(n)
#
# 2. Space complexity:
# - str(num) creates a new string: O(n)
# - replace(...) creates another string: O(n)
# - int(...) processes another copy (internally): O(n)
# => Overall: O(n)


# ===== Without string conversion =====
# - Let say num = ab|6cd6ef
# - Flip the left-most 6 and it becomes ab|9cd6ef
# - We can see that num is increase by 900000 - 600000 = 3*10^5
#   in which 5 is the position of the left-most 6
#   (count from the right, start from 0)


def max_num_from_69(num: int) -> int:
    max_num = num
    position = 0  # right to left
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


# ===== Complexity =====
# Let n = number of digits
#
# 1. Time complexity: O(n) - for finding the left-most 6
# 2. Space complexity: O(1)
