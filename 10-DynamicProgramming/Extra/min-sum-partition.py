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
- Absolute difference of 2 sums: |S1 - S2| = |2*S1 - S|
-> Problem: Choose elements into 'set1' such that |2*S1 - S| is minimized.

Identify DP problem:
- Related to optimization.
- Can be broken down into a sequence of decisions for each arr[i]
  (include or not include in 'set1').
- Can reach the same state from multiple paths:
  Example: arr = [10, 5, 3, 2]    (traversing backward)
  . skip 2, skip 3, take 5 -> (i = 0, current_sum = 5)
  . take 2, take 3, skip 5 -> (i = 0, current_sum = 5)

Idea:
- Let dp(i, curr_sum) be the minimum absolute difference between S1 and S2
  after allocating all items from 'arr' into 2 sets,
  with curr_sum be sum(set1) after allocating items from arr[i+1..n-1] into 2 sets.
- At ith element, there are 2 options:
  . Add to set1: ans = dp(i - 1, curr_sum + arr[i]) 
  . Add to set2: ans = dp(i - 1, curr_sum) (sum(set1) doesn't change)
  -> Pick the minimum answer.
- Base case: 
  . i == -1 (all items have been processed)
    -> Return diff = |2*S1 - S| = |2*curr_sum - total_sum|
- Final result: dp(i=n-1, curr_sum=0)
  . No items after arr[n-1] to allocate into 2 sets.
    -> curr_sum = sum(set1) = 0
"""

# ===== Top-down =====
from functools import cache


def min_difference_td(arr: list[int]) -> int:
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
- Number of DP states: O(n * total_sum)
  . may skip multiple states (jump from curr_sum to curr_sum + arr[i])

2. Space complexity: O(n * total_sum)
- cache: O(n * total_sum)
- recursion stack: O(n)
"""


# ===== Bottom-up =====
"""
Alternative:
- Let dp(i, curr_sum) be the minimum absolute difference between S1 and S2
  after allocating all items from 'arr' into 2 sets,
  with curr_sum be sum(set1) after allocating items from arr[0..i-1] into 2 sets.
- At ith element, there are 2 options:
  . Add to set1: ans = dp(i + 1, curr_sum + arr[i]) 
  . Add to set2: ans = dp(i + 1, curr_sum) (sum(set1) doesn't change)
  -> Pick the minimum answer.
- Base case: 
  . i == n (all items have been processed)
    -> Return diff = |2*S1 - S| = |2*curr_sum - total_sum|
- Final result: dp(i=0, curr_sum=0)
  . No items before arr[0] to allocate into 2 sets.
    -> curr_sum = sum(set1) = 0
"""


def min_difference_bu(arr: list[int]) -> int:
    n = len(arr) - 1
    total_sum = sum(arr)

    # dp[i][curr_sum]: maximum absolute difference between S1 and S2
    # after allocating all items from 'arr' into 2 sets,
    # with curr_sum = sum(set1) after allocating items from arr[0..i-1] into 2 sets.
    dp = [[0] * (total_sum + 1) for _ in range(n + 1)]

    # base case: dp[n][S1] = |2*S1 - S|
    for curr_sum in range(total_sum + 1):
        dp[n][curr_sum] = abs(2 * curr_sum - total_sum)

    for i in range(n - 1, -1, -1):
        for curr_sum in range(total_sum + 1):
            # Option 1: add arr[i] to set2
            dp[i][curr_sum] = dp[i + 1][curr_sum]

            # Option 2: add arr[i] to set1
            if curr_sum + arr[i] > total_sum:
                break
            dp[i][curr_sum] = min(dp[i][curr_sum], dp[i + 1][curr_sum + arr[i]])

            if i == 0:
                break  # only need to populate dp[0][0]

    return dp[0][0]


"""
Complexity:
1. Time complexity: O(n * total_sum)
2. Space complexity: O(n * total_sum) for 'dp'
"""


# ===== Bottom-up: Optimize space =====
"""
- dp[i] only depends on dp[i + 1]
  -> only track the last 2 rows
"""


def min_difference_bu_v2(arr: list[int]) -> int:
    n = len(arr) - 1
    total_sum = sum(arr)

    # base case: dp[n][S1] = |2*S1 - S|
    dp = [abs(2 * curr_sum - total_sum) for curr_sum in range(total_sum + 1)]

    for i in range(n - 1, -1, -1):
        # Option 1: add arr[i] to set2
        # . dp[i][curr_sum] = dp[i + 1][curr_sum]
        next_dp = dp[:]

        # Option 2: add arr[i] to set1
        for curr_sum in range(total_sum + 1):
            if curr_sum + arr[i] > total_sum:
                break
            next_dp[curr_sum] = min(next_dp[curr_sum], dp[curr_sum + arr[i]])

            if i == 0:
                break  # only need to populate dp[0][0]

        dp = next_dp

    return dp[0]  # dp[0][0]


"""
Complexity:
1. Time complexity: O(n * total_sum)
2. Space complexity: O(total_sum) for 'dp' and 'next_dp'
"""


# ===== Bottom-up: Optimize space (further) =====
"""
- next_dp[s] only depends on dp[s] and dp[s+arr[i]]
  -> After next_dp[s] is populated, dp[s] is not touched again.
  -> Overwrite to the same 'dp' array.
"""


def min_difference_bu_v3(arr: list[int]) -> int:
    n = len(arr) - 1
    total_sum = sum(arr)

    # base case: dp[n][S1] = |2*S1 - S|
    dp = [abs(2 * curr_sum - total_sum) for curr_sum in range(total_sum + 1)]

    for i in range(n - 1, -1, -1):
        # Option 1: add arr[i] to set2
        # . dp[i][curr_sum] = dp[i + 1][curr_sum]

        # Option 2: add arr[i] to set1
        for curr_sum in range(total_sum + 1):
            if curr_sum + arr[i] > total_sum:
                break

            # overwrite is safe (dp[i][higher_s] entries don't use dp[i+1][s])
            dp[curr_sum] = min(dp[curr_sum], dp[curr_sum + arr[i]])

            if i == 0:
                break  # only need to populate dp[0][0]

    return dp[0]  # dp[0][0]


"""
Complexity:
1. Time complexity: O(n * total_sum)
2. Space complexity: O(total_sum) for 'dp'
"""


if __name__ == "__main__":
    for arr, expected in [
        ([1, 6, 11, 5], 1),
        ([1, 4], 3),
        ([1], 1),
    ]:
        for fn in [
            min_difference_td,
            min_difference_bu,
            min_difference_bu_v2,
            min_difference_bu_v3,
        ]:
            assert fn(arr) == expected
