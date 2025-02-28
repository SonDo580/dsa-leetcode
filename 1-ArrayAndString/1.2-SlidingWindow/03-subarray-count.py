# Given an array of positive integers nums and an integer k, 
# return the number of subarrays where the product of all the elements 
# in the subarray is strictly less than k.
# 
# For example, given the input nums = [10, 5, 2, 6], k = 100, 
# the answer is 8. The subarrays with products less than k are:
# 
# [10], [5], [2], [6], [10, 5], [5, 2], [2, 6], [5, 2, 6]

def subarray_count(nums: list[int], k: int) -> int:
    if k <= 1:
        return 0
    
    left = 0
    count = 0
    current_product = 1

    for right in range(len(nums)):
        current_product *= nums[right]

        while current_product >= k:
            current_product //= nums[left]
            left += 1

        # the (additional) number of valid subarrays is the window length
        count += right - left + 1    

    return count