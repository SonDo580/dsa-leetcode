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

# ===== Analyze =====
# To build all permutations, we can select all elements at first index.
# For the second index, we can select all remaining elements. And so on.
# => Number of permutations: n * (n - 1) * ... * 1 = n!


# ===== Recursive divide-and-conquer =====
def get_permutations(nums: list[int]) -> list[list[int]]:
    # 1 element -> 1 permutation
    if len(nums) == 1:
        return [nums]

    result: list[list[int]] = []  # store all possible permutations

    for i in range(len(nums)):
        # find all permutations of remaining numbers
        rest_permutations = get_permutations(nums[:i] + nums[(i + 1):])

        # combine current number with permutations of remaining numbers
        for permutation in rest_permutations:
            result.append([nums[i]] + permutation)
    
    return result

# Time complexity:
# Let T(n) be the time complexity for an input of size n
# - Iterate through the list of numbers: O(n)
# - In each iteration:
#   + creating a new list without the current element: O(n)
#   + recursively call get_permutations on the new list: T(n - 1)
#   + combining result: O((n-1)!) (rest_permutations size)
# => T(n) = O(n^2) + O(n)*T(n-1) + O(n(n-1)!)
#         = O(n!) + O(n)*T(n-1) 
# - O(n)*T(n-1) = O(n) * O(n - 1) * O(n - 2) * ... * T(1)
#   T(1) = O(1) (return the result right away)
# => T(n) = O(n!)
  
# Space complexity: O(n!)
# - result array: 
#   + number of permutations is n!
#   + each permutation has length n
#   -> O(n*n!) = O(n!) 
# - recursion stack: O(n)
#   (the function recursively calls itself until n == 1)
