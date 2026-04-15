"""
Given an integer array 'nums',
an array 'queries' where queries[i] = [x, y] and an integer 'limit',
return a boolean array that represents the answer to each query.

A query is true if the sum of the subarray from x to y
is less than limit, or false otherwise.

For example, given nums = [1, 6, 3, 2, 7, 2],
queries = [[0, 3], [2, 5], [2, 4]], and limit = 13,
the answer is [true, false, true].
For each query, the subarray sums are [12, 14, 12].
"""

"""
- Brute-force approach would take O(n * m)
"""


# ===== Prefix sum =====
def answer_queries(nums: list[int], queries: list[int], limit: int) -> list[bool]:
    # prefix_sum[i] = sum([0..i])
    prefix_sum = [nums[0]]
    for i in range(1, len(nums)):
        prefix_sum.append(nums[i] + prefix_sum[-1])

    ans: list[bool] = []
    for x, y in queries:
        # . sum([x..y]) = prefix_sum[y] - prefix_sum[x - 1]
        # . sum([x..y]) = prefix_sum[y] - prefix_sum[x] + nums[x]
        # -> use the second formula to avoid dealing with x = 0
        sum = prefix_sum[y] - prefix_sum[x] + nums[x]
        ans.append(sum < limit)

    return ans


"""
Complexity:
- Let n = len(nums), m = len(queries)

1. Time complexity: O(n + m)
- Build prefix_sum array: O(n)
- m queries, answer each query takes O(1)
-> Total: O(n + m)

2. Space complexity: O(n) for prefix_sum
"""
