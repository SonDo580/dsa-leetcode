# Given an integer array nums of unique elements,
# return all possible subsets (the power set).

# The solution set must not contain duplicate subsets.
# Return the solution in any order.

# Example 1:
# Input: nums = [1,2,3]
# Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

# Example 2:
# Input: nums = [0]
# Output: [[],[0]]

# Constraints:
# 1 <= nums.length <= 10
# -10 <= nums[i] <= 10
# All the numbers of nums are unique.


# ===== Analyze =====
# - Let n = nums.length
# - The problem is asking for the combinations of nums
#   -> there are 2^n combinations
# - The number of elements in each combination is from 0 to n


# ===== Recursive divide-and-conquer =====
# - Add the empty set
# - Loop through each item:
#   + build the combinations that starts with current item
#     by prepending it to each combination of remaining items.
#   + because order doesn't matter in a combination,
#     only combine current element and elements that come after it.
def subsets(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = [[]]

    for i in range(len(nums)):
        remaining_combinations = subsets(nums[(i + 1) :])
        for combination in remaining_combinations:
            result.append([nums[i]] + combination)

    return result
