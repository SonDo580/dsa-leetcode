"""
https://www.geeksforgeeks.org/problems/0-1-knapsack-problem0945/1

Given two arrays, val[] and wt[],
where each element represents the value and weight of an item respectively,
and an integer W representing the maximum capacity of the knapsack (the total weight it can hold).

The task is to put the items into the knapsack such that
the total value obtained is maximum without exceeding the capacity W.
Return the maximum total value obtained.

Note: You can either include an item completely or exclude it entirely —
fractional selection of items is not allowed. Each item is available only once.
"""

"""
Identify DP problems:
1. Optimal substructure:
- The problem can be broken down into a sequence of decisions for each item i:
  include or exclude it.
- The maximum value we can obtain with capacity w using items up to index i
  depends on optimal solutions to smaller versions of the same problem. 

2. Overlapping subproblem:
- The same state is encountered through different combinations of previous choices
- Example: weights = [2, 3, 5, ...], W = 10
  . take item0 (2), take item1 (3), skip item2 (5)
    next subproblem: start from item3, remaining capacity = 10 - 2 - 3 = 5
  . skip item0 (2), skip item1 (3), take item2 (5)
    next subproblem: start from item3, remaining capacity = 10 - 5 = 5
  -> both paths lead to the same subproblem.
"""

"""
- Let dp(i, w) be the maximum value we can obtains from items[0..i],
  with knapsack's capacity w.
- The final result is dp(n - 1, W).
- Base case: i == -1 -> ans = 0 (no elements to use)
- At each ith item, we have 2 options:
  . skip: ans = dp(i - 1, w)
  . take: ans = dp(i - 1, w - weights[i]) + values[i]
  . pick the action that results in maximum value
  -> dp(i) = max(dp(i - 1, w), dp(i - 1, w - weights[i]) + values[i])
"""


# ===== Top-down =====
from functools import cache


def knap_sack(W: int, weights: list[int], values: list[int]) -> int:
    @cache
    def dp(i: int, w: int) -> int:
        if i == -1:
            return 0

        # Option 1: skip ith item
        ans = dp(i - 1, w)

        # Option 2: take ith item
        if w >= weights[i]:
            ans = max(ans, dp(i - 1, w - weights[i]) + values[i])

        return ans

    n = len(weights)  # = len(values)
    return dp(n - 1, W)


"""
Complexity:

1. Time complexity: O(n * W)

2. Space complexity: O(n * W)
- memoization table: O(n * W)
- recursion stack: O(n)
"""

# ===== Bottom-up: TODO =====
# ===== Bottom-up (optimize space): TODO =====
