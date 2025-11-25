"""
https://leetcode.com/problems/longest-subsequence-with-limited-sum

You are given an integer array 'nums' of length n,
and an integer array queries of length m.

Return an array answer of length m where answer[i] is the maximum size of a subsequence
that you can take from nums such that the sum of its elements is less than or equal to queries[i].

A subsequence is an array that can be derived from another array by
deleting some or no elements without changing the order of the remaining elements.

Example 1:
Input: nums = [4,5,2,1], queries = [3,10,21]
Output: [2,3,4]
Explanation: We answer the queries as follows:
- The subsequence [2,1] has a sum less than or equal to 3. It can be proven that 2 is the maximum size of such a subsequence, so answer[0] = 2.
- The subsequence [4,5,1] has a sum less than or equal to 10. It can be proven that 3 is the maximum size of such a subsequence, so answer[1] = 3.
- The subsequence [4,5,2,1] has a sum less than or equal to 21. It can be proven that 4 is the maximum size of such a subsequence, so answer[2] = 4.

Example 2:
Input: nums = [2,3,4,5], queries = [1]
Output: [0]
Explanation: The empty subsequence is the only subsequence that has a sum less than or equal to 1, so answer[0] = 0.

Constraints:
n == nums.length
m == queries.length
1 <= n, m <= 1000
1 <= nums[i], queries[i] <= 10^6
"""

"""
Analysis:
- To maximize the number of items in a subsequence,
  we should always accumulate the smallest item at any step.
  Stop when the sum exceed query.
- Finding the smallest item randomly at each step takes O(n). 
  But the problem doesn't ask for the exact subsequence, only its size.
  -> We can sort 'nums' in ascending order.
     Then for each query, iterate sequentially to accumulate items.

Optimization:
- Calculate the prefix sum for sorted 'nums' in advance.
- Constraint note: 1 <= nums[i] <= 10^6 
  -> prefix_sum array is strictly increasing.
- For each query, perform binary search to find the "insertion point"
  (index where prefix sum starts exceeding 'query').
- The size of the subsequence is the number of items up to that point.
"""


def answer_queries(nums: list[int], queries: list[int]) -> list[int]:
    def _get_prefix_sum_arr(arr: list[int]) -> list[int]:
        prefix_sum: list[int] = []
        current_sum = 0
        for num in arr:
            current_sum += num
            prefix_sum.append(current_sum)
        return prefix_sum

    def _binary_search(prefix_sum: list[int], num: int) -> int:
        """Return the index where prefix sum starts exceeding num."""
        left = 0
        right = len(prefix_sum) - 1

        while left <= right:
            mid = (left + right) // 2
            current = prefix_sum[mid]

            if current == num:
                # prefix_sum is strictly increasing -> we can stop right away
                return mid + 1

            if current > num:
                right = mid - 1  # search left portion
            else:
                left = mid + 1  # search right portion

        return left

    nums.sort()
    prefix_sum_arr = _get_prefix_sum_arr(nums)

    answers: list[int] = []
    for query in queries:
        insertion_point = _binary_search(prefix_sum_arr, query)
        answers.append(insertion_point)

    return answers


"""
Complexity:

1. Time complexity:
- Sort nums: O(n*log(n))
- Calculate prefix sum for nums: O(n)
- Loop through queries: m times
  + perform binary search in each iteration: O(log(n))
=> Overall: O((m + n) * log(n))

2. Space complexity:
- sort 'nums' (depends on the algorithm): Python's timsort takes O(n)
- prefix_sum: O(n)
=> Overall: O(n)
"""
