# Given an integer array nums and an integer k,
# find the sum of the subarray with the largest sum whose length is k.

# => fixed-length window

def subarray_max_sum(nums: list[int], k: int) -> int:
    # build the first window
    current_sum = 0
    for i in range(k):
        current_sum += nums[i]

    # initialize max_sum to the sum of the first window
    max_sum = current_sum

    # slide the window along the array
    # (add the right element & remove the left element)
    for i in range(k, len(nums)):
        current_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, current_sum)

    return max_sum
