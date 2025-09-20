# Given an array nums of distinct integers,
# return all the possible permutations.
# You can return the answer in any order.

# Example 1:
# Input: nums = [1,2,3]
# Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

# Example 2:
# Input: nums = [0,1]
# Output: [[0,1],[1,0]]

# Example 3:
# Input: nums = [1]
# Output: [[1]]

# Constraints:
# 1 <= nums.length <= 6
# -10 <= nums[i] <= 10
# All the integers of nums are unique.


# ===== Strategy =====
# - To build all permutations, we can have n choices for the first position.
# - For the second position, we can n - 1 remaining choices. And so on.
# => Number of permutations: n * (n - 1) * ... * 1 = n!


def get_permutations(nums: list[int]) -> list[list[int]]:
    # Base case: 1 element -> 1 permutation
    if len(nums) == 1:
        return [nums]

    all_permutations: list[list[int]] = []

    for i in range(len(nums)):
        # Find all permutations of remaining numbers (exclude current number)
        rest_permutations = get_permutations(nums[:i] + nums[(i + 1) :])

        # Combine current number with permutations of remaining numbers
        for permutation in rest_permutations:
            all_permutations.append([nums[i]] + permutation)

    return all_permutations


# ===== Complexity =====
# 1. Time complexity:
# Let T(n) be the time complexity for an input of size n
# - Iterate through the list of numbers: O(n)
# - In each iteration:
#   + creating a new list without the current element: O(n)
#   + recursively call get_permutations on the new list: T(n - 1)
#   + combining result: O((n - 1)!) (rest_permutations size)
# => T(n) = O(n) * (O(n) + T(n - 1) + O((n - 1)!))
#         = O(n^2) + O(n) * T(n - 1) + O(n * (n - 1)!)
#         = O(n!) + O(n) * T(n - 1)
# . T(n - 1) = O((n - 1)!) + O(n - 1) * T(n - 2)
#   T(n - 2) = O((n - 2)!) + O(n - 2) * T(n - 3)
#   ...
#   T(1) = O(1) (return the result right away)
# . O(n) * T(n - 1) = O(n) * O((n - 1)!) +
#                     O(n) * O(n - 1) * T(n - 2)
#                   = O(n!) +
#                     O(n * (n - 1)) * O((n - 2)!) +
#                     O(n) * O(n - 1) * O(n - 2) * T(n - 3)
#                   = ...
#                   = (n - 1) * O(n!) +
#                     O(n) * O(n - 1) * O(n - 2) * ... * T(1)
#                   = (n - 1) * O(n!) +
#                     O(n) * O(n - 1) * O(n - 2) * ... * O(1)
#                   = O(n * n!)
# => T(n) = O(n!) + O(n * n!) = O(n * n!)
#
# 2. Space complexity:
# - result array: O(n * n!)
#   + number of permutations is n!
#   + each permutation has length n
# - recursion stack: O(n)
#   (the function recursively calls itself until n == 1)
# => Overall: O(n * n!)


# ===== Approach 2 =====
# - Build each permutation using a recursive function backtrack(current),
#   where current is the permutation being built.
# - The base case is when current.length = nums.length (the permutation is completed).
#   -> add 'current' to the result list
# - To build all permutations, we need all elements at the first index. and for each of those elements,
#   we need all the other element at the second index, and so on.
#   -> each 'backtrack' call needs to loop through all elements,
#      except for those that have been used in 'current'.
def get_permutations(nums: list[int]) -> list[list[int]]:
    all_permutations: list[list[int]] = []

    def backtrack(current: list[int]):
        if len(current) == len(nums):
            # - We mutate 'current' across 'backtrack' calls,
            #   -> create a copy of 'current' when adding
            all_permutations.append(current[:])
            return

        for num in nums:
            if num not in current:
                current.append(num)
                backtrack(current)
                current.pop()

    backtrack([])
    return all_permutations
