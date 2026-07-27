"""
https://leetcode.com/problems/greatest-common-divisor-of-strings/

For two strings s and t, we say "t divides s" if and only if
s = t + t + t + ... + t + t (i.e., t is concatenated with itself one or more times).

Given two strings str1 and str2, return the largest string x such that x divides both str1 and str2.
"""

"""
Idea:
- x must be a common prefix of both strings 
  -> Try all common prefixes.
     For each prefix, check if both strings divide it.
- Record length of the GCD so far.
  Only slice string at the end.
"""


def _is_divisor(s: str, i: int) -> bool:
    """Check if s[..i] divides s."""
    n = len(s)
    if n % (i + 1) != 0:
        return False

    for j in range(i + 1, n):
        if s[j] != s[j % (i + 1)]:
            return False

    return True


class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        gcd_len = 0
        m = len(str1)
        n = len(str2)

        for i in range(min(m, n)):
            if str1[i] != str2[i]:
                break
            if _is_divisor(str1, i) and _is_divisor(str2, i):
                gcd_len = i + 1

        return str1[:gcd_len]


"""
Complexity:
1. Time complexity: O(min(m, n) * (m + n))
2. Space complexity: O(1)
"""


# === Improvement ===
"""
- If s1 and s2 have a common divisible substring,
  repeating them in different orders should produce the same string:
  . s1 + s2 = s2 + s1
- Let the smallest common divisible substring be P
  . str1 = m*P
  . str2 = n*P
- Any common divisible substring T must also divides P
  . T = d*P
  T divides str1 -> d divides m
  T divides str2 -> d divides n
  -> d is common divisor of m and n
  -> max_d = GCD(m, n) correspond to greatest common divisible substring. 
"""


def _gcd(a: int, b: int) -> int:
    return a if b == 0 else _gcd(b, a % b)


class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        if str1 + str2 != str2 + str1:
            return ""

        gcd_len = _gcd(len(str1), len(str2))
        return str1[:gcd_len]


"""
Complexity:
- Let m = len(str1), n = len(str2)

1. Time complexity: O(m + n)
- String concatenation: O(m + n)
- Find GCD: O(log(min(m, n)))
- String slicing (get result): O(min(m, n))

2. Space complexity: O(m + n) for concatenated strings
"""
