# Given an integer array nums of unique elements,
# return all possible subsets (the power set).
#
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


# ===== Analysis =====
# - Let n = nums.length
# - The problem is asking for all the combinations of nums
#   -> there are 2^n combinations
# - The number of elements in each combination is from 0 to n

# ===== Strategy =====
# - Add the empty set
# - Loop through each item:
#   + build the combinations that starts with current item
#     by prepending it to each combination of remaining items.
#   + because order doesn't matter in a combination,
#     only combine current element and elements that come after it.


def get_subsets(nums: list[int]) -> list[list[int]]:
    all_subsets: list[list[int]] = [[]]

    for i in range(len(nums)):
        remaining_subsets = get_subsets(nums[(i + 1) :])
        for subset in remaining_subsets:
            all_subsets.append([nums[i]] + subset)

    return all_subsets


# ===== Approach 2 =====
# - Build each subset using a recursive function backtrack(current, i),
#   where 'current' is the subset being built,
#   i is the index that represents where we should start iterating.
# - We need i to avoid duplicates. Because order doesn't matter in a subset,
#   only combine current element and elements that come after it.
# - Since the subsets can have any length, every "node" is an answer
#   (including the root []).


def get_subsets(nums: list[int]) -> list[list[int]]:
    all_subsets: list[list[int]] = []

    def backtrack(current: list[int], i: int):
        # - We mutate 'current' across 'backtrack' calls,
        #   -> create a copy of 'current' when adding
        all_subsets.append(current[:])

        if i == len(nums):
            return

        for j in range(i, len(nums)):
            current.append(nums[j])
            backtrack(current, j + 1)
            current.pop()

    backtrack([], 0)
    return all_subsets
