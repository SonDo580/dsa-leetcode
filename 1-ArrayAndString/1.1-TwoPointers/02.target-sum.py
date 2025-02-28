# Given a sorted array of unique integers and a target integer,
# return true if there exists a pair of numbers that sum to target,
# false otherwise.
# For example, given nums = [1, 2, 4, 6, 8, 9, 14, 15] and target = 13,
# return true because 4 + 9 = 13.

def target_sum(nums: list[int], target: int) -> bool:
    left = 0
    right = len(nums) - 1

    while left < right:
        sum = nums[left] + nums[right]
        if sum == target:
            return True
        elif sum > target:
            right -= 1
        else:
            left += 1

    return False
