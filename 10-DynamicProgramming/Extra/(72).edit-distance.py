"""
https://leetcode.com/problems/edit-distance/

Given two strings word1 and word2,
return the minimum number of operations required to convert word1 to word2.

You have the following three operations permitted on a word:
- Insert a character
- Delete a character
- Replace a character
"""

"""
Identify DP problem:
1. Optimal substructure
- The problem can be broken down into smaller decisions based on
  the last (or first) character of the strings.
- If word1[i] = word2[j], no operations needed 
  -> cost = cost of the remaining strings
- Otherwise, choose the best (minimum cost) of 3 operations.

2. Overlapping subproblem:
- Many different sequences of operations lead to the same pair of substrings
- Example: word1 = "horse", word2 = "ros"
  . delete "h" -> must solve "orse" -> "ros" next
    insert "r" to the front -> must solve "rorse" -> "ros" next
    match "r" at the front -> must solve "orse" -> "os" next
  . replace "h" with "r" -> must solve "orse" -> "os" next
"""

"""
- Let dp(i, j) be the minimum number of operations required
  to convert word1[0..i-1] to word2[0..j-1]
- Then dp(len(word1), len(word2)) is the result.
- Base case:
  . i == 0 -> insert j characters of word2[0..j-1]
  . j == 0 -> delete i characters of word1[0..i-1]
- Recurrence relation:
  (note that we are matching the last character in the substrings)
  . word1[i-1] == word2[j-1] -> dp(i, j) = dp(i-1, j-1)
    (characters match -> the cost is the same as matching prefixes)
  . otherwise, choose the one with minimum cost among 3 operations:
    . delete: dp(i-1, j) + 1
      (delete word1[i-1] from s1
       -> word1[i-1]: resolved, word2[j-1]: waiting to be processed)
    . insert: dp(i, j-1) + 1      
      (append word2[j-1] to s1 then move both cursors left once
       -> word2[j-1]: resolved, word1[i-1]: waiting to be processed)
    . replace: dp(i-1, j-1) + 1
      (convert word1[i-1] to word2[j-1], then move both cursors left once
       -> both characters are resolved)
"""


# ===== Top-down =====
from functools import cache


def min_distance(word1: str, word2: str) -> int:
    @cache
    def dp(i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i
        if word1[i - 1] == word2[j - 1]:
            return dp(i - 1, j - 1)
        return min(dp(i - 1, j), dp(i, j - 1), dp(i - 1, j - 1)) + 1

    return dp(len(word1), len(word2))


"""
Complexity:
- Let m = len(word1), n = len(word2)

1. Time complexity: O(m * n)

2. Space complexity: O(m * n)
- memoization table: O(m * n)
- recursion stack: O(m + n)
"""


# ===== Bottom-up =====
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[-1] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

    return dp[m][n]


"""
Complexity:

1. Time complexity: O(m * n)

2. Space complexity: O(m * n) for 'dp'
"""


# ===== Bottom-up (optimize space) =====
"""
- The result of each cell only depends on the left, top, and top-left cells.
  -> Only need to track the last 2 rows.
"""


def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    prev_dp = [-1] * (n + 1)

    for i in range(m + 1):
        dp = [-1] * (n + 1)

        for j in range(n + 1):
            if i == 0:
                dp[j] = j
            elif j == 0:
                dp[j] = i
            elif word1[i - 1] == word2[j - 1]:
                dp[j] = prev_dp[j - 1]
            else:
                dp[j] = min(prev_dp[j], dp[j - 1], prev_dp[j - 1]) + 1

        prev_dp = dp

    return prev_dp[n]


"""
Complexity:

1. Time complexity: O(m * n)

2. Space complexity: O(n) for 'dp' and 'prev_dp'
"""
