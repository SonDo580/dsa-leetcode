"""
Given an integer array 'nums' and an integer k,
find the sum of the subarray with the largest sum whose length is k.
"""

"""
Monotonicity of window constraint (keep size=k):
- extend right: increase size
- shrink left: decrease size
"""


def subarray_max_sum(nums: list[int], k: int) -> int:
    # initialize max sum to the sum of the first window
    current_sum = 0
    for i in range(k):
        current_sum += nums[i]
    max_sum = current_sum

    # keep the window size k while sliding
    # (add element i, remove element i-k)
    for i in range(k, len(nums)):
        current_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, current_sum)

    return max_sum


"""
Complexity: 
- Let n = len(nums)
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
