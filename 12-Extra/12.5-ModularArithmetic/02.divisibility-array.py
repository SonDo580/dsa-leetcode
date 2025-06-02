# You are given a 0-indexed string word of length n consisting of digits,
# and a positive integer m.
# The divisibility array div of word is an integer array of length n such that:
# div[i] = 1 if the numeric value of word[0,...,i] is divisible by m, or
# div[i] = 0 otherwise.
# Return the divisibility array of word.

# Example 1:
# Input: word = "998244353", m = 3
# Output: [1,1,0,0,0,1,1,0,0]
# Explanation: There are only 4 prefixes that are divisible by 3: "9", "99", "998244", and "9982443".

# Example 2:
# Input: word = "1010", m = 10
# Output: [0,1,0,1]
# Explanation: There are only 2 prefixes that are divisible by 10: "10", and "1010".

# Constraints:
# 1 <= n <= 10^5
# word.length == n
# word consists of digits from 0 to 9
# 1 <= m <= 10^9


# ===== Analyze =====
# The simplest way:
# - Iterate over 'word'
# - At each index i:
#   + convert the prefix string into an integer
#   + check if that integer is divisible by m
# - Convert a string to an integer takes O(n) where n is the length of the string
#   -> Time complexity: 1 + 2 + ... + n = n(n + 1) / 2 -> O(n^2)
#
# => Improvement 1:
# - Store the built number. Start with current_num = 0
# - Every time we append a digit: current_num = previous_num * 10 + digit
# - This is still inefficient since the final number will be very large:
#   n = 10^5 -> final number is on the order of 10^(10^5)
#
# => Improvement 2:
# - Instead of tracking the whole number, only track the remainder
#   current_remainder = (previous_remainder * 10 + digit) % m
#
# - Formula (see note.md):
#   1. (a + b) mod n = ((a mod n) + b) mod n
#   2. ab mod n = (a mod n).b mod n
#
# - Proof:
# current_remainder
# = current_num % m
# = (previous_num * 10 + digit) % m
# = ((previous_num * 10) % m + digit) % m
# = (((previous_num % m) * 10) % m + digit) % m
# = ((previous_remainder * 10) % m + digit) % m
# = (previous_remainder * 10 + digit) % m


def divisibility_array(word: str, m: int) -> list[int]:
    divisibility = []
    current_remainder = 0

    for digit in word:
        current_remainder = (current_remainder * 10 + int(digit)) % m
        divisibility.append(1 if current_remainder == 0 else 0)

    return divisibility


# ===== Complexity =====
# Time complexity: O(n) - iterating through 'word'
# Space complexity: O(n) - divisibility array
