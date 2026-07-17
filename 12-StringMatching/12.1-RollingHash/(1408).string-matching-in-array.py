"""
https://leetcode.com/problems/string-matching-in-an-array/

Given an array of string 'words',
return all strings in 'words' that are a substring of another word.
You can return the answer in any order.
"""

"""
Idea:
- For each word, check if it's a substring of other words.
- To check substring, see '(28).index-of-substring':
  . method 1: brute-force
  . method 2: rolling hash (Rabin-Karp)
"""


def stringMatching(words: list[str]) -> list[str]:
    n = len(words)
    ans: list[int] = []

    for i in range(n):
        for j in range(n):
            if j == i:
                continue
            # if _is_substr_v1(words[i], words[j]):
            if _is_substr_v2(words[i], words[j]):
                ans.append(words[i])
                break

    return ans


def _match(text: str, i: int, pattern: str) -> bool:
    """
    Return True if text[i..i+len(pattern)-1] == 'pattern'.
    Ensure valid window before calling this function.
    """
    for j in range(len(pattern)):
        if text[i + j] != pattern[j]:
            return False
    return True


# === brute-force ===
def _is_substr_v1(pattern: str, text: str) -> bool:
    """Return True if 'pattern' is substring of 'text'."""
    for i in range(len(text) - len(pattern) + 1):
        if _match(text, i, pattern):
            return True
    return False


# === rolling hash ===
"""
Rabin-Karp hash function:
. hash(s) = (s[0]*p^(n-1) + s[1]*p^(n-2) + ... + s[n-1]*p^0) % q
  . p is a small base
    -> pick 2 for easy power calculation (by shifting bits)
  . q is a larger prime number to avoid overflow and reduce collisions
    -> pick 1e9 + 7
- Calculate hash of the 1st window [0..L]
  . hash(s[0..L]) = (s[0]*p^(L-1) + s[1]*p^(L-2) + ... + s[L-1]*p^0) % q
  . hash(s[0..L+1]) = (s[0]*p^L + s[1]*p^(L-1) + ... + s[L]*p^0) % q
                    = (p * hash(s[0..L]) + s[L]) % q
  . base case: hash(s[0..0]) = s[0] % q

- Recalculate hash when sliding fixed-size window:
  . hash(s[i..L]) 
    = (s[i]*p^(L-1) + s[i+1]*p^(L-2) + ... + s[i+L-1]*p^0) % q
  . hash(s[i+1..L+1]) 
    = (s[i+1]*p^(L-1) + s[i+2]*p^(L-2) + ... + s[i+L]*p^0) % q
    = (p * (hash(s[i..L]) - s[i]*p^(L-1)) + s[i+L]) % q
    -> . calculate p^(L-1) % q in advance
       . normalize: add q if result < 0
"""


def _is_substr_v2(pattern: str, text: str) -> bool:
    """Return True if 'pattern' is substring of 'text'."""
    n = len(text)
    L = len(pattern)
    if L > n:
        return False

    # Choose constants for hash function
    p = 2
    q = int(1e9 + 7)

    # Precompute p^(L-1) % q
    power = 1
    for _ in range(L - 1):
        power = (power * p) % q

    # Compute hash values for pattern and 1st window of text
    pattern_hash = ord(pattern[0]) % q
    window_hash = ord(text[0]) % q
    for i in range(1, L):
        pattern_hash = (p * pattern_hash + ord(pattern[i])) % q
        window_hash = (p * window_hash + ord(text[i])) % q

    # Slide window and compare
    for i in range(n - L + 1):
        # Only compare characters for possible match
        if window_hash == pattern_hash and _match(text, i, pattern):
            return True

        # Compute hash value for next window
        if i < n - L:
            window_hash = (
                p * (window_hash - ord(text[i]) * power) + ord(text[i + L])
            ) % q
            if window_hash < 0:
                # Normalize into range [0, q)
                window_hash += q

    return False


"""
Complexity:
- Let n = len(words)
      l = len(words[i])
    
1. Time complexity: O(n^2) * O(is_substr)
- is_substr_v1 (brute-force):
  . l1 = len(pattern), l2 = len(word)
  . check l2-l1+1 windows, each takes O(l1)
  -> total: O((l2-l1)*l1) = O(l^2)
- is_substr_v2 (rolling hash):
  . check l2-l1+1 windows.
  . skip invalid window if hash values don't match: O(1)
  . compare characters when hash values match: O(l1)
    (only once and return, if the hash function is good)
  -> total: O(l2 + l1) = O(l)

2. Space complexity: O(1)
"""
