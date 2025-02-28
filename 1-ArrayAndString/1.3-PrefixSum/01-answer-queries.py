# Given an integer array nums,
# an array queries where queries[i] = [x, y] and an integer limit,
# return a boolean array that represents the answer to each query.
#
# A query is true if the sum of the subarray from x to y
# is less than limit, or false otherwise.
#
# For example, given nums = [1, 6, 3, 2, 7, 2],
# queries = [[0, 3], [2, 5], [2, 4]], and limit = 13,
# the answer is [true, false, true].
# For each query, the subarray sums are [12, 14, 12].

def answer_queries(nums: list[int], queries: list[int], limit: int) -> list[bool]:
    # build the prefix sum array in O(n)
    prefix_sum = [nums[0]]
    for i in range(1, len(nums)):
        prefix_sum.append(nums[i] + prefix_sum[-1])

    # answer each query in O(1)
    answers = []
    for x, y in queries:
        # sum_of_subarray = prefix_sum[y] - prefix_sum[x - 1]
        # use the following formula to avoid dealing with the left bound
        sum = prefix_sum[y] - prefix_sum[x] + nums[x]
        answers.append(sum < limit)

    return answers

# n: nums length; m: queries length

# Time complexity: O(n + m)
# Space complexity: O(n) - to build the prefix_sum array

# Calculate without the prefix sum
# Time complexity: O(n * m)