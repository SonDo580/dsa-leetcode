# The next greater element of some element x in an array is the first greater element that is to the right of x in the same array.
# You are given two distinct 0-indexed integer arrays nums1 and nums2, where nums1 is a subset of nums2.
# For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] and determine the next greater element of nums2[j] in nums2.
# If there is no next greater element, then the answer for this query is -1.
# Return an array ans of length nums1.length such that ans[i] is the next greater element as described above.

# Example 1:
# Input: nums1 = [4,1,2], nums2 = [1,3,4,2]
# Output: [-1,3,-1]
# Explanation: The next greater element for each value of nums1 is as follows:
# - 4 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.
# - 1 is underlined in nums2 = [1,3,4,2]. The next greater element is 3.
# - 2 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.

# Example 2:
# Input: nums1 = [2,4], nums2 = [1,2,3,4]
# Output: [3,-1]
# Explanation: The next greater element for each value of nums1 is as follows:
# - 2 is underlined in nums2 = [1,2,3,4]. The next greater element is 3.
# - 4 is underlined in nums2 = [1,2,3,4]. There is no next greater element, so the answer is -1.

# Constraints:
# 1 <= nums1.length <= nums2.length <= 1000
# 0 <= nums1[i], nums2[i] <= 10^4
# All integers in nums1 and nums2 are unique.
# All the integers of nums1 also appear in nums2.

# Follow up: Could you find an O(nums1.length + nums2.length) solution?


# ===== Strategy =====
# - We can use a monotonically decreasing stack and push elements of nums2 onto it.
# - Keep popping elements off the stack if the top number is less than current number.
# - Check if the number exists in nums1 and retrieve the index i in nums1.
# - Update answers[i] if it is -1 (don't update again if it's already set).
# - Since all values in each array are unique, we can build a dictionary
#   that map value to index for nums1 (for faster lookup).


def next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    # Initialize answers
    answers: list[int] = [-1] * len(nums1)

    # Build a dictionary to lookup the index of a value in nums1
    index_dict_1: dict[int, int] = {}
    for i, num in enumerate(nums1):
        index_dict_1[num] = i

    # A monotonically decreasing stack
    stack = []

    for current_num in nums2:
        # Keep popping element off the stack if they are less than current num
        while len(stack) > 0 and stack[-1] < current_num:
            num = stack.pop()

            # Check if num exists in nums1.
            if num in index_dict_1:
                # Retrieve the index of num in nums1
                i = index_dict_1[num]

                # Set the next greater element for nums1[i]
                # Only update answer if it has not been set
                if answers[i] == -1:
                    answers[i] = current_num

        stack.append(current_num)

    return answers


# ===== Complexity =====
# Let m = nums1.length; n = nums2.length
#
# 1. Time complexity:
# - Initialize answers: O(m)
# - Build index dictionary: O(m)
# - Loop through nums2: O(n)
#   + Each iteration is amortized O(1), since the inner while loop can run at most n times
#     (each element is pushed on the stack exactly once, and popped from the stack at most once)
#
# 2. Space complexity:
# - O(m) for the answers list
# - O(m) for the index dictionary
# - O(n) for the stack
# => Overall: O(m + n)


# ===== Possible optimization =====
# - Count the number of times we've set answer
# - We can stop when count == nums1.length
# - Note that this does not reduce complexity
