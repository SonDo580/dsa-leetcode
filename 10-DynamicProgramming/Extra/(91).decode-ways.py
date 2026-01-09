"""
https://leetcode.com/problems/decode-ways/

You have intercepted a secret message encoded as a string of numbers.
The message is decoded via the following mapping:
"1" -> 'A'
"2" -> 'B'
...
"25" -> 'Y'
"26" -> 'Z'

However, while decoding the message,
you realize that there are many different ways you can decode the message
because some codes are contained in other codes ("2" and "5" vs "25").

For example, "11106" can be decoded into:
. "AAJF" with the grouping (1, 1, 10, 6)
. "KJF" with the grouping (11, 10, 6)
. The grouping (1, 11, 06) is invalid because "06" is not a valid code (only "6" is valid).

Note: there may be strings that are impossible to decode.

Given a string s containing only digits, return the number of ways to decode it.
If the entire string cannot be decoded in any valid way, return 0.

The test cases are generated so that the answer fits in a 32-bit integer.
"""

"""
Analysis:
- At each character i, there are 2 ways to decode:
  . As single digit. Condition: s[i] != 0 
  . As leading digit of a 2-digit number. 
    Condition: i + 1 < len(s) and (s[i] == 1 or s[i] == 2 and s[i + 1] <= 6)

- Let dp(i) be the number of ways to decode s[i..n-1] where n = len(s)
- Recurrence relation:
  . dp(i) = 0
  . dp(i) += dp(i + 1) if s[i] != 0
  . dp(i) += dp(i + 2) if i + 1 < len(s) and (s[i] == 1 or s[i] == 2 and s[i + 1] <= 6)
- Base case: dp(n) = 1 (empty string)
- The answer to the problem is dp(0)
"""

# ===== Top-down DP =====
from functools import cache


def num_encodings(s: str) -> int:
    @cache
    def dp(i: int) -> int:
        """Return number of ways to decode s[i..n-1]."""
        if i == len(s):
            return 1

        count = 0
        if s[i] != "0":
            # single digit
            count += dp(i + 1)
        if i + 1 < len(s) and (s[i] == "1" or s[i] == "2" and s[i + 1] <= "6"):
            # 2 digits
            count += dp(i + 2)
        return count

    return dp(0)


"""
Complexity:
- Let n = len(s)

1. Time complexity: O(n) (each state is computed once)

2. Space complexity: O(n) for memoization table and recursion stack
"""


# ===== Bottom-up DP =====
def num_encodings(s: str) -> int:
    n = len(s)
    dp: list[int] = [0] * (n + 1)
    dp[n] = 1

    for i in range(n - 1, -1, -1):
        if s[i] != "0":
            dp[i] += dp[i + 1]
        if i + 1 < n and (s[i] == "1" or s[i] == "2" and s[i + 1] <= "6"):
            dp[i] += dp[i + 2]

    return dp[0]


"""
Complexity:
1. Time complexity: O(n)

2. Space complexity: O(n) for 'dp'
"""


# ===== Bottom-up DP (optimize space) =====
def num_encodings(s: str) -> int:
    n = len(s)
    prev2 = 1  # as dp[i + 2]
    prev1 = 0 if s[n - 1] == "0" else 1  # as dp[i + 1]

    for i in range(n - 2, -1, -1):
        curr = 0  # as dp[i]
        if s[i] != "0":
            curr += prev1
        if s[i] == "1" or s[i] == "2" and s[i + 1] <= "6":
            curr += prev2
        prev1, prev2 = curr, prev1

    return prev1


"""
Complexity:
1. Time complexity: O(n)

2. Space complexity: O(1)
"""
