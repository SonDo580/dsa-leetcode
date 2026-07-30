"""
https://leetcode.com/problems/edit-distance/

Given two strings 'word1' and 'word2',
return the minimum number of operations required to convert 'word1' to 'word2'.

You have the following three operations permitted on a word:
- Insert a character
- Delete a character
- Replace a character
"""

"""
Identify DP problem:
- Optimization: find minimum number of operations
- Broken down into sequence of decisions at each character. 
  Local decision affects future decisions.
- Multiple sequences of operations lead to the same state.
  Example: word1 = "horse", word2 = "ros"
  . delete word1[0] -> ("orse", "ros")
    prepend "r" to word1 -> ("rorse", "ros")
    match word1[0] and word2[0] -> ("orse", "os")
  . replace word1[0] with "r" -> ("orse", "os")

Idea:
- Let dp(i, j) be the minimum number of operations required
  to convert word1[0..i-1] to word2[0..j-1].
- Result: dp(len(word1), len(word2)).
- Base case:
  . i == 0 -> insert j characters of word2[0..j-1]
  . j == 0 -> delete i characters of word1[0..i-1]
- Recurrence relation:
  Consider the last character in each substring.
  . word1[i-1] == word2[j-1]    (characters match)
    -> no operations required
    -> dp(i, j) = dp(i-1, j-1)
       (cost = cost to match prefixes)
  . Otherwise, choose the one with minimum cost among 3 operations:
    . delete: dp(i-1, j) + 1
      (delete word1[i-1])
    . insert: dp(i, j-1) + 1      
      (append word2[j-1] then move both cursors left)
    . replace: dp(i-1, j-1) + 1
      (convert word1[i-1] to word2[j-1] then move both cursors left)
"""


# ===== Top-down =====
from functools import cache


def min_distance(word1: str, word2: str) -> int:
    @cache
    def dp(i: int, j: int) -> int:
        """Min cost to convert word1[0..i-1] into word2[0..j-1]"""
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
- cache: O(m * n)
- recursion stack: O(m + n)
"""


# ===== Bottom-up =====
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    dp = [[-1] * (n + 1) for _ in range(m + 1)]
    # -1 is just dummy value, any other value also works (will be overwritten anyway)

    # base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    # i = j = 0 -> dp[0][0] = 0 (set in both loops)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

    return dp[m][n]


"""
Complexity:
1. Time complexity: O(m * n)
2. Space complexity: O(m * n) for 'dp'
"""


# ===== Bottom-up: Optimize space =====
"""
- The result of each cell only depends on the left, top, and top-left cells.
  -> Only need to track the last 2 rows.
"""


def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # base case: dp[0][j] = j
    dp = [j for j in range(n + 1)]  # dp[0]

    for i in range(1, m + 1):
        next_dp = [-1] * (n + 1)

        for j in range(n + 1):
            if j == 0:
                # dp[i][0] = i
                next_dp[j] = i
            elif word1[i - 1] == word2[j - 1]:
                # dp[i][j] = dp[i-1][j-1]
                next_dp[j] = dp[j - 1]
            else:
                # dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                next_dp[j] = min(dp[j], next_dp[j - 1], dp[j - 1]) + 1

        dp = next_dp

    return dp[n]  # dp[m][n]


"""
Complexity:
1. Time complexity: O(m * n)
2. Space complexity: O(n) for 'dp' and 'next_dp'
"""


# ===== Bottom-up: Optimize space (further) =====
"""
- Overwrite to the same 'dp' array.
- Save dp[j-1] to a variable before overwriting.
"""


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)

        # base case: i = 0 -> dp[j] = j
        dp = [j for j in range(n + 1)]

        for i in range(1, m + 1):
            saved = dp[0]  # prev_dp[j-1] for next j iteration
            dp[0] = i

            for j in range(1, n + 1):
                next_saved = dp[j]  # save before overwriting

                if word1[i - 1] == word2[j - 1]:
                    # dp[j] = prev_dp[j-1]
                    dp[j] = saved
                else:
                    # dp[j] = min(prev_dp[j], dp[j-1], prev_dp[j-1]) + 1
                    # . dp[j] hasn't been overwritten <-> prev_dp[j]
                    dp[j] = min(dp[j], dp[j - 1], saved) + 1

                saved = next_saved

        return dp[n]  # dp[m][n]


"""
Complexity:
1. Time complexity: O(m * n)
2. Space complexity: O(n) for 'dp'
"""


# ===== Top-down (alternative) =====
"""
- Let dp(i, j) be the minimum number of operations required
  to convert word1[i..m-1] to word2[j..n-1].
- Result: dp(0, 0).
- Base case:
  . i == m -> insert n-j characters of word2[j..n-1]
  . j == n -> delete m-i characters of word1[i..m-1]
- Recurrence relation:
  Consider the 1st character in each substring.
  . word1[i] == word2[j]    (characters match)
    -> no operations required
    -> dp(i, j) = dp(i+1, j+1)
       (cost = cost to match suffixes)
  . Otherwise, choose the one with minimum cost among 3 operations:
    . delete: dp(i+1, j) + 1
      (delete word1[i])
    . insert: dp(i, j+1) + 1    
      (prepend word2[j] then move both cursors right)
    . replace: dp(i+1, j+1) + 1
      (convert word1[i] to word2[j] then move both cursors right)
"""


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m = len(word1)
        n = len(word2)

        @cache
        def dp(i: int, j: int) -> int:
            """Min cost to convert word1[i..m-1] into word2[j..n-1]"""
            if i == m:
                return n - j
            if j == n:
                return m - i
            if word1[i] == word2[j]:
                return dp(i + 1, j + 1)
            return min(dp(i + 1, j), dp(i, j + 1), dp(i + 1, j + 1)) + 1

        return dp(0, 0)


"""
Complexity:

1. Time complexity: O(m * n)

2. Space complexity: O(m * n)
- cache: O(m * n)
- recursion stack: O(m + n)
"""
