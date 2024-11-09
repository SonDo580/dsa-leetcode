# Given an array of positive integers nums and an integer k, find the length 
# of the longest subarray whose sum is less than or equal to k.

from typing import List

def longest_run(nums: List[int], k: int) -> int:
    left = 0
    current_sum = 0
    max_length = 0

    for right in range(len(nums)):
        # add new element to the window  
        current_sum += nums[right]

        # if the window becomes invalid, 
        # we may have to remove multiple elements from the left
        while current_sum > k:
            current_sum -= nums[left]
            left += 1

        # the current window is now valid 
        # update max_length if needed
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Time complexity: O(n) 
# - Maximum: 2n iterations
#   + the right pointer move n times
#   + the left pointer move n times

# Amortized analysis:
# - the inner while loop that move the left pointer
#   can only iterate at most n times for the entire algorithm
# - although the worst case for an iteration is O(n)
#   it averages out to O(1)
