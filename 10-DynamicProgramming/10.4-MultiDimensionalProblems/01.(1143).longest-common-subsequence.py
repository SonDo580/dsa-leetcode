"""
https://leetcode.com/problems/longest-common-subsequence/

Given two strings text1 and text2,
return the length of their longest common subsequence.
If there is no common subsequence, return 0.

A subsequence of a string is a new string generated
from the original string with some characters (can be none) deleted
without changing the relative order of the remaining characters.

For example, "ace" is a subsequence of "abcde".
A common subsequence of two strings is a subsequence that is common to both strings.
"""

"""
Identifying DP problem:
- asking for the longest subsequence
- using a letter affects future letters we can take 
  (can only use letters that come after it)

Solution:
- Let dp(i, j) returns the length of the longest common subsequence
  if we start at i of text1 and j of text2
- For each pair (i, j) there are 2 possibilities:
  . text1[i] == text2[j]: 
    We found a match and should use it to increase the length.
    After matching, move to the next character in both strings:
    -> dp(i, j) = 1 + dp(i + 1, j + 1)
  . text1[i] != text2[j]: 
    We can move to the next character in text1 or text2
    -> try both and get the maximum length
    -> dp(i, j) = max(dp(i + 1, j), dp(i, j + 1))
- Base case:
  . i = text1.length OR j = text2.length
  -> no common characters (because 1 string has no characters remaining) 
  -> return 0
"""


# ===== Top-down =====
from functools import cache


def longest_common_subsequence(text1: str, text2: str) -> int:
    @cache
    def dp(i: int, j: int) -> int:
        if i == len(text1) or j == len(text2):
            return 0

        if text1[i] == text2[j]:
            return 1 + dp(i + 1, j + 1)
        return max(dp(i + 1, j), dp(i, j + 1))

    return dp(0, 0)


"""
Complexity:
- Let n = len(text1), m = len(text2)

1. Time complexity: O(m * n)

2. Space complexity: O(m * n)
- memoization table: O(m * n)
- recursion stack: O(m + n)
"""


# ===== Bottom-up =====
def longest_common_subsequence(text1: str, text2: str) -> int:
    n = len(text1)
    m = len(text2)

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    # cover base cases implicitly: dp[_][m] = dp[n][_] = 0

    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if text1[i] == text2[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])

    return dp[0][0]


"""
Complexity:

1. Time complexity: O(m * n)

2. Space complexity: O(m * n) for 'dp'
"""


# ===== Bottom-up (optimize space) =====
"""
dp[i][j] depends on dp[i + 1][j + 1], dp[i + 1][j], dp[i][j + 1]
(bottom-right, bottom, right)
-> we only need to keep track of current row and last row.
-> use 2 arrays
"""


def longest_common_subsequence(text1: str, text2: str) -> int:
    n = len(text1)
    m = len(text2)

    prev_dp = [0] * (m + 1)  # as dp[i + 1]
    for i in range(n - 1, -1, -1):
        dp = [0] * (m + 1)  # as dp[i]

        for j in range(m - 1, -1, -1):
            if text1[i] == text2[j]:
                dp[j] = 1 + prev_dp[j + 1]
            else:
                dp[j] = max(prev_dp[j], dp[j + 1])

        prev_dp = dp

    return prev_dp[0]


"""
Complexity:

1. Time complexity: O(m * n)

2. Space complexity: O(m) for 'dp' and 'prev_dp'
"""


# ===== Bottom-up (optimize space further) =====
"""
- Once dp[i + 1][j + 1] and dp[i][j + 1] is "used" by dp[i][j],
  we don't need them anymore.
  dp[i + 1][j] with serve as the bottom-right of dp[i][j - 1]
-> Use 1 array and modify it in place,
   and 1 extra variable to preserve dp[i + 1][j].
"""


def longest_common_subsequence(text1: str, text2: str) -> int:
    n = len(text1)
    m = len(text2)

    dp = [0] * (m + 1)
    for i in range(n - 1, -1, -1):
        prev_bottom_right = dp[m]  # as dp[i + 1][j + 1]
        for j in range(m - 1, -1, -1):
            temp = dp[j]  # save dp[i + 1][j]
            if text1[i] == text2[j]:
                # dp[i][j] = 1 + dp[i + 1][j + 1]
                dp[j] = 1 + prev_bottom_right
            else:
                # dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
                dp[j] = max(dp[j], dp[j + 1])
            prev_bottom_right = temp

    return dp[0]


"""
Complexity:

1. Time complexity: O(m * n)

2. Space complexity: O(m) for 'dp'
"""


# ===== Extra: Find 1 LCS =====
def longest_common_subsequence(text1: str, text2: str) -> int:
    n = len(text1)
    m = len(text2)

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if text1[i] == text2[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])

    # Backtrack to find 1 LCS
    i, j = 0, 0
    lcs: list[str] = []

    while i < n and j < m:
        if text1[i] == text2[j]:
            # characters match -> this character is part of the LCS
            lcs.append(text1[i])
            i += 1
            j += 1
        else:
            # move in the direction of larger DP value
            if dp[i + 1][j] >= dp[i][j + 1]:
                i += 1
            else:
                j += 1

    print("LCS: ", "".join(lcs))
    return dp[0][0]


"""
Complexity:

1. Time complexity: O(m * n)
- DP: O(m * n)
- backtrack: O(m + n)

2. Space complexity: O(m * n) for 'dp'
! Note that we must keep the full 2D table for backtracking.
"""


# ===== Find all LCSs =====
# TODO