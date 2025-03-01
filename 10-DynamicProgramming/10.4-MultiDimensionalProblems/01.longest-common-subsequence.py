# Given two strings text1 and text2, 
# return the length of their longest common subsequence. 
# If there is no common subsequence, return 0.

# A subsequence of a string is a new string generated 
# from the original string with some characters (can be none) deleted 
# without changing the relative order of the remaining characters.

# For example, "ace" is a subsequence of "abcde".
# A common subsequence of two strings is a subsequence that is common to both strings.

# Example 1:
# Input: text1 = "abcde", text2 = "ace" 
# Output: 3  
# Explanation: The longest common subsequence is "ace" and its length is 3.

# Example 2:
# Input: text1 = "abc", text2 = "abc"
# Output: 3
# Explanation: The longest common subsequence is "abc" and its length is 3.

# Example 3:
# Input: text1 = "abc", text2 = "def"
# Output: 0
# Explanation: There is no such common subsequence, so the result is 0.

# Constraints:
# 1 <= text1.length, text2.length <= 1000
# text1 and text2 consist of only lowercase English characters.


# ===== Identifying DP problem =====
# - asking for the longest subsequence
# - using a letter affects future letters we can take 
#   (can only use letters that come after it)

# ===== Analyzing =====
# - state variables: i and j for text1 and text2
# - dp(i, j): return the length of the longest common subsequence
#             if we start at i of text1 and j of text2
#  
# - At each pair (i, j) there are 2 possibilities:
# + text1[i] == text2[j]: 
#   We found a match and should use it to increase the length
#   After matching, move to the next character in both strings:
#   -> dp(i, j) = 1 + dp(i + 1, j + 1)
# + text1[i] != text2[j]: 
#   We can move to the next character in text1 or text2
#   -> try both and get the maximum length
#   -> dp(i, j) = max(dp(i + 1, j), dp(i, j + 1))
# 
# - Base case:
# If i = text1.length OR j = text2.length
# -> no common characters (because 1 string has no characters remaining) 
# -> return 0


# ===== Top-down =====
def longest_common_subsequence(text1: str, text2: str) -> int:
    def dp(i: int, j: int) -> int:
        if i == len(text1) or j == len(text2):
            return 0
        
        key = (i, j)
        if key in cache:
            return cache[key]
        
        if text1[i] == text2[j]:
            cache[key] = 1 + dp(i + 1, j + 1)
        else:
            cache[key] = max(dp(i + 1, j), dp(i, j + 1))

        return cache[key]

    cache: dict[tuple[int, int], int] = {}
    return dp(0, 0)

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

# Time complexity: O(n*m)
# Space complexity: O(n*m)