# Given two strings s and t, return true if s is a subsequence of t,
# or false otherwise.
#
# A subsequence of a string is a sequence of characters
# that can be obtained by deleting some (or none)
# of the characters from the original string, while maintaining
# the relative order of the remaining characters
#
# For example, "ace" is a subsequence of "abcde" while "aec" is not.


def is_subsequence(s: str, t: str) -> bool:
    i = 0
    j = 0

    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1

    return i == len(s)
