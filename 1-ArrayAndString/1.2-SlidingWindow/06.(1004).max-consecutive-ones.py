"""
https://leetcode.com/problems/max-consecutive-ones-iii/

Given a binary array nums and an integer k, 
return the maximum number of consecutive 1's in the array 
if you can flip at most k 0's.
"""

"""
Reframe the question:
- Return length of the longest sub-array that contains at most k zeros

Monotonicity of window constraint:
- Extend right (may) increase the number of 0's.
  Shrink left (may) decrease the number of 0's
"""

def longest_ones(nums: list[int], k: int) -> int:
    left = 0
    count_zero = 0
    max_length = 0

    for right in range(len(nums)):
        if nums[right] == 0:
            count_zero += 1

        while count_zero > k:
            if nums[left] == 0:
                count_zero -= 1
            left += 1
        
        max_length = max(max_length, right - left + 1)

    return max_length


"""
Complexity:

1. Time complexity: O(n)
- 'right' moves n times.
- 'left' moves at most n times.

2. Space complexity: O(1)
"""
