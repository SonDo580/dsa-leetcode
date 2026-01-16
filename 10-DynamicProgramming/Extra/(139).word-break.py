"""
https://leetcode.com/problems/word-break/

Given a string s and a dictionary of strings 'wordDict',
return true if s can be segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the segmentation.
"""

"""
Idea:
- Try if we can segment 1 word, then recursively do the same with the remaining part.
- Each part may be encountered multiple times -> memoize the result to avoid recomputation.

DP:
- Let dp(i) returns True if s[i..n-1] can be segmented into words in 'wordDict'.
  Then dp(0) represents the results for the full string.
- Try all s[i..j] to until a word in dictionary is found.
  Recursively do the same with s[j+1..n-1].
-> Recurrence relation:
  . dp(i) = any(word[i:j+1] in wordDict AND dp(j + 1) == True) 
- If no words can be segmented from the current position, return False.
- Base case: i == n -> segmented s fully -> return True

Optimization:
- Convert the list 'wordDict' to a set for fast lookup.
  We can also use a trie.
- Record max length of words in 'wordDict' for upper bound of j 
  . j = min(i + L, n)

Note:
- We cannot optimize space complexity for Bottom-up approach
  because the recurrence relation is not static.
"""


# ===== Top-down DP + set =====
from functools import cache


def word_break(s: str, word_dict: list[str]) -> bool:
    n = len(s)
    word_set: set[str] = set(word_dict)
    max_len = max(len(w) for w in word_dict)

    @cache
    def dp(i: int) -> bool:
        """
        Return True if s[i..n-1] can be segmented into words in dictionary.
        Otherwise return False.
        """
        if i == n:
            return True

        for j in range(i, min(i + max_len, n)):
            if s[i : j + 1] in word_set and dp(j + 1):
                return True
        return False

    return dp(0)


"""
Complexity:
- Let n = len(s), m = len(word_dict), L = max_len

1. Time complexity: O(m*L + n*L^2)
- Convert 'wordDict' to set: O(m * L)
- Find max word length in 'wordDict': O(m)
- Number of DP states: O(n)
  Each DP state has a for loop:
  . number of iterations: O(L)
  . string slicing (word): O(L)
  -> total DP: O(n * L^2)

2. Space complexity: O(m*L + n)
- 'word_set': O(m * L)
- dp's memoization table: O(n)
- dp's recursion stack: O(n)
"""


# ===== Bottom-up DP + set =====
def word_break(s: str, word_dict: list[str]) -> bool:
    n = len(s)
    word_set: set[str] = set(word_dict)
    max_len = max(len(w) for w in word_dict)

    dp = [False] * (n + 1)
    dp[n] = True
    for i in range(n - 1, -1, -1):
        for j in range(i, min(i + max_len, n)):
            if dp[j + 1] and s[i : j + 1] in word_set:
                dp[i] = True
                break

    return dp[0]


"""
Complexity:

1. Time complexity: O(m*L + n*L^2)

2. Space complexity: O(m*L + n)
- 'word_set': O(m * L)
- dp: O(n)
"""


# ===== Top-down DP + trie =====
class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_word: bool = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_word = True


def word_break(s: str, word_dict: list[str]) -> bool:
    n = len(s)
    trie = Trie()
    max_len = -1
    for word in word_dict:
        trie.insert(word)
        max_len = max(max_len, len(word))

    @cache
    def dp(i: int) -> bool:
        if i == n:
            return True

        curr = trie.root
        for j in range(i, min(i + max_len, n)):
            if s[j] not in curr.children:
                break

            curr = curr.children[s[j]]
            if curr.is_word and dp(j + 1):
                return True
        return False

    return dp(0)


"""
Complexity:

1. Time complexity: O(m*L + n*L)
- Build trie from 'wordDict': O(m * L)
- Find max word length in 'wordDict': O(m)
- Number of DP states: O(n)
  Each DP state has a for loop:
  . number of iterations: O(L)
  . character matching in trie: O(1)
  -> total DP: O(n * L)

2. Space complexity: O(m*L + n)
- trie: O(m * L)
- dp's memoization table: O(n)
- dp's recursion stack: O(n)
"""


# ===== Bottom-up DP + trie =====
def word_break(s: str, word_dict: list[str]) -> bool:
    n = len(s)
    trie = Trie()
    max_len = -1
    for word in word_dict:
        trie.insert(word)
        max_len = max(max_len, len(word))

    dp = [False] * (n + 1)
    dp[n] = True
    for i in range(n - 1, -1, -1):
        curr = trie.root
        for j in range(i, min(i + max_len, n)):
            if s[j] not in curr.children:
                break

            curr = curr.children[s[j]]
            if curr.is_word and dp[j + 1]:
                dp[i] = True
                break

    return dp[0]


"""
Complexity:

1. Time complexity: O(m*L + n*L)

2. Space complexity: O(m*L + n)
- trie: O(m * L)
- dp: O(n)
"""
