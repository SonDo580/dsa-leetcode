"""
https://www.geeksforgeeks.org/problems/minimum-sum-partition3317/1

Given an array arr[] containing non-negative integers, divide it into 2 sets
set1 and set2 such that the absolute difference between their sums is minimum.
Return the minimum difference.
"""

"""
Analysis:
- Total sum of all elements in 'arr' is S
  Total sum of all elements in 'set1' is S1
  Total sum of all elements in 'set2' is S2 = S - S1
- Absolute difference of 2 sums: |S1 - S2| =  |2*S1 - S|
  To minimize this, we need to find all possible values of S1
  that can be formed from elements in 'arr'.

Identify DP problem: (note that we're going backward)
1. Optimal substructure:
- Problem: find minimum absolute difference between 2 sets using the first i items,
  with current sum for set1 be curr_sum.
- At each ith item, there are 2 options:
  . include arr[i] in set1 
    -> subproblem: first i - 1 items, curr_sum = curr_sum + arr[i]
  . include arr[i] in set2 
    -> subproblem: first i - 1 items, curr_sum is the same

2. Overlapping subproblem:
- Example: arr = [10, 5, 3, 2]
  . skip 2, skip 3, take 5 -> next problem: i = 10, current_sum = 5
  . take 2, take 3, skip 5 -> next problem: i = 10, current_sum = 5
"""

"""
- Let dp(i, curr_sum) returns the minimum absolute difference after 
  dividing arr[0..i] into 2 sets, with curr_sum be the current sum of set1.
- We need to divide all elements of 'arr', and set1 is initially empty.
  -> Result is dp(i=n-1, curr_sum=0)
- At ith element, there are 2 options:
  . add to set1: ans = dp(i - 1, curr_sum + arr[i]) 
  . add to set2: ans = dp(i - 1, curr_sum)
  . pick the minimum answer 
- Base case:
  . i == -1
    -> all elements have been processed 
    -> return the absolute difference between 2 sets: |2*curr_sum - total_sum|
"""

# ===== Top-down =====
from functools import cache


def min_difference(arr: list[int]) -> int:
    total_sum = sum(arr)

    @cache
    def dp(i: int, curr_sum: int) -> int:
        if i == -1:
            return abs(2 * curr_sum - total_sum)

        # Option 1: add arr[i] to set1
        take = dp(i - 1, curr_sum + arr[i])

        # Option 2: add arr[i] to set2
        skip = dp(i - 1, curr_sum)

        return min(take, skip)

    return dp(len(arr) - 1, 0)


"""
Complexity:
- Let n = len(arr), total_sum = sum(arr)

1. Time complexity: O(n * total_sum)

2. Space complexity: O(n * total_sum)
- memoization table: O(n * total_sum)
- recursion stack: O(n)
"""


# ===== Bottom-up =====
import math


def min_difference(arr: list[int]) -> int:
    n = len(arr) - 1
    total_sum = sum(arr)

    dp = [[0] * (total_sum + 1) for _ in range(n)]
    for curr_sum in range(total_sum + 1):
        dp[-1][curr_sum] = abs(2 * curr_sum - total_sum)

    for i in range(n):
        for curr_sum in range(total_sum, -1, -1):
            # Option 1: add arr[i] to set2
            dp[i][curr_sum] = dp[i - 1][curr_sum]

            # Option 2: add arr[i] to set1
            if curr_sum + arr[i] <= total_sum:
                dp[i][curr_sum] = min(dp[i][curr_sum], dp[i - 1][curr_sum + arr[i]])

    return dp[n - 1][0]


"""
Complexity:

1. Time complexity: O(n * total_sum)

2. Space complexity: O(n * total_sum) for 'dp'
"""


# ===== Bottom-up (optimize space) =====
"""
- dp[i] only depends on dp[i - 1]
  -> only track the last 2 rows
"""


def min_difference(arr: list[int]) -> int:
    n = len(arr) - 1
    total_sum = sum(arr)

    prev_dp = [0] * (total_sum + 1)
    for curr_sum in range(total_sum + 1):
        prev_dp[curr_sum] = abs(2 * curr_sum - total_sum)

    for i in range(n):
        dp = [0] * (total_sum + 1)

        for curr_sum in range(total_sum, -1, -1):
            # Option 1: add arr[i] to set2
            dp[curr_sum] = prev_dp[curr_sum]

            # Option 2: add arr[i] to set1
            if curr_sum + arr[i] <= total_sum:
                dp[curr_sum] = min(dp[curr_sum], prev_dp[curr_sum + arr[i]])

        prev_dp = dp

    return prev_dp[0]


"""
Complexity:

1. Time complexity: O(n * total_sum)

2. Space complexity: O(total_sum) for 'dp' and 'prev_dp'
"""
