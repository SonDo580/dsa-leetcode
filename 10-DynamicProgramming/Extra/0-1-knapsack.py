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
Identify DP problem:
- Optimization: find max value obtainable (without exceeding capacity)
- The problem can be broken down into a sequence of decisions for each item.
- The same state is encountered through multiple paths.
  Example: weights = [2, 3, 5, ...], W = 10
  . take 2, take 3, skip 5 -> remaining capacity = 10 - 2 - 3 = 5
  . skip 2, skip 3, take 5 -> remaining capacity = 10 - 5 = 5

Idea:
- Let dp(i, w) be the maximum value we can obtain from items[0..i],
  with knapsack's capacity w.
- Final result: dp(n - 1, W).
- Base case: i == -1 -> ans = 0 (no elements to use)
- At each item i, we have 2 options:
  . skip: ans = dp(i - 1, w)
  . take: ans = dp(i - 1, w - weights[i]) + values[i]
  -> dp(i) = max(skip_ans, take_ans)
"""


# === Top-down ===
from functools import cache


def knap_sack_td(W: int, val: list[int], wt: list[int]) -> int:
    @cache
    def dp(i: int, w: int) -> int:
        """Max value obtainable from items[0..i] given capacity w."""
        if i == -1:
            return 0

        # Option 1: skip ith item
        ans = dp(i - 1, w)

        # Option 2: take ith item
        if w >= wt[i]:
            ans = max(ans, dp(i - 1, w - wt[i]) + val[i])

        return ans

    n = len(wt)  # = len(val)
    return dp(n - 1, W)


"""
Complexity:
- Number of DP states: O(n * W)

1. Time complexity: O(n * W)

2. Space complexity: O(n * W)
- cache: O(n * W)
- recursion stack: O(n)
"""


# === Bottom-up===
"""

Alternative:
- Let dp(i, w) be the maximum value we can obtain from items[i..n-1],
  with knapsack's capacity w.
- Final result: dp(0, W).
- Base case: i == n -> ans = 0 (no elements to use)
- At each item i, we have 2 options:
  . skip: ans = dp(i + 1, w)
  . take: ans = dp(i + 1, w - weights[i]) + values[i]
  -> dp(i) = max(skip_ans, take_ans)
"""


def knap_sack_bu(W: int, val: list[int], wt: list[int]) -> int:
    n = len(val)  # = len(wt)

    # dp[i][w]: max value obtainable from items[i..n-1] given capacity w
    # base case: dp[n][_] = 0
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(n - 1, -1, -1):
        for w in range(W, -1, -1):
            # option 1: skip ith item
            dp[i][w] = dp[i + 1][w]

            # option 2: take ith item
            if w >= wt[i]:
                dp[i][w] = max(dp[i][w], dp[i + 1][w - wt[i]] + val[i])

            if i == 0:
                break  # only need to populate dp[0][W]

    return dp[0][W]


"""
Complexity:
1. Time complexity: O(n * W)
2. Space complexity: O(n * W) for 'dp'
"""


# === Bottom-up: Optimize space ===
"""
- dp[i] only depends on dp[i + 1]
  -> use 2 1D arrays, don't need the whole matrix
"""


def knap_sack_bu_v1(W: int, val: list[int], wt: list[int]) -> int:
    n = len(val)  # = len(wt)

    # dp[i][w]: max value obtainable from items[i..n-1] given capacity w
    dp = [0] * (W + 1)  # base case: dp[n][_] = 0

    for i in range(n - 1, -1, -1):
        # option 1: skip ith item
        # . dp[i][w] = dp[i + 1][w]
        next_dp = dp[:]

        # option 2: take ith item
        for w in range(W, -1, -1):
            if w >= wt[i]:
                next_dp[w] = max(next_dp[w], dp[w - wt[i]] + val[i])
            if i == 0:
                break  # only need to populate dp[0][W]

        dp = next_dp

    return dp[W]  # dp[0][W]


"""
Complexity:
1. Time complexity: O(n * W)
2. Space complexity: O(W) for 'dp' and 'next_dp'
"""


# === Bottom-up: Optimize space (further) ===
"""
- next_dp[w] only depends on dp[w] and dp[w-wt[i]]
  (equal and less weight entries)
  -> After populating next_dp[w], dp[w] is not needed anymore.
  -> Overwrite to the same 'dp' array.
"""


def knap_sack_bu_v2(W: int, val: list[int], wt: list[int]) -> int:
    n = len(val)  # = len(wt)

    # dp[i][w]: max value obtainable from items[i..n-1] given capacity w
    dp = [0] * (W + 1)  # base case: dp[n][_] = 0

    for i in range(n - 1, -1, -1):
        # option 1: skip ith item
        # . dp[i][w] = dp[i + 1][w]

        # option 2: take ith item
        for w in range(W, -1, -1):
            if w >= wt[i]:
                # overwrite is safe (dp[i][lower_w] entries don't use dp[i+1][w])
                dp[w] = max(dp[w], dp[w - wt[i]] + val[i])

            if i == 0:
                break  # only need to populate dp[0][W]

    return dp[W]  # dp[0][W]


"""
Complexity:
1. Time complexity: O(n * W)
2. Space complexity: O(W) for 'dp'
"""


# === Compare top-down and bottom-up ===
"""
- Top-down:
  . allow skipping multiple states when the weights are large.
- Bottom-up:
  . can optimize space to O(W).
  . no stack overflow.
  . array access is faster than (function call + hashmap lookup).
"""


if __name__ == "__main__":
    for W, val, wt, expected in [
        (4, [1, 2, 3], [4, 5, 1], 3),
        (3, [1, 2, 3], [4, 5, 6], 0),
        (5, [10, 40, 30, 50], [5, 4, 2, 3], 80),
    ]:
        for fn in [knap_sack_td, knap_sack_bu, knap_sack_bu_v1, knap_sack_bu_v2]:
            assert fn(W, val, wt) == expected
