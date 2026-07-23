"""
https://leetcode.com/problems/plus-one/

You are given a large integer represented as an integer array 'digits',
where each digits[i] is the ith digit of the integer.
The digits are ordered from most significant to least significant in left-to-right order.
The large integer does not contain any leading 0's.

Increment the large integer by one and return the resulting array of digits.
"""

"""
Idea:
- Iterate through 'digits' in reverse.
- If digits[i] + 1 < 10, update digits[i] = digits[i] + 1 and return 'digits'.
- If digits[i] + 1 == 10, update digits[i] = 0 and continue adding 1 to digits[i-1].
  If i == 0, prepend 1 to 'digits'.
"""


class Solution:
    def plusOne(self, digits: list[int]) -> list[int]:
        n = len(digits)
        for i in range(n - 1, -1, -1):
            if digits[i] + 1 < 10:
                digits[i] += 1
                break

            digits[i] = 0

            # === carrying ===
            if i == 0:
                digits.insert(0, 1)
                break
            # else: add 1 to digits[i-1] (next iteration)

        return digits


"""
Complexity:
- Let n = len(digits)

1. Time complexity: O(n)
- Iterate through 'digits': O(n)
- (May) insert at the front: O(n)

2. Space complexity: O(1) (mutate 'digits')
"""
