"""
https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/

Given two strings `needle` and `haystack`,
return the index of the first occurrence of `needle` in `haystack`,
or -1 if `needle` is not part of `haystack`.
"""

# ===== Brute-force =====
# =======================
"""
- From each position in `haystack`, 
  check if subsequent characters match `needle`.
"""


def index_of(haystack: str, needle: str) -> int:
    for i in range(len(haystack) - len(needle) + 1):
        if _match(haystack, i, needle):
            return i
    return -1


def _match(text: str, i: int, pattern: str) -> bool:
    """
    Return True if text[i..i+len(pattern)-1] equals `pattern`.
    Ensure valid window before calling this function.
    """
    for j in range(len(pattern)):
        if text[i + j] != pattern[j]:
            return False
    return True


"""
Complexity:
- Let n = len(haystack)
      m = len(needle)

1. Time complexity: O((n - m) * m)

2. Space complexity: O(1)
"""


# ===== Rabin-Karp =====
# =======================
"""
General idea:
- Compute a hash for `needle` and each window of `haystack`
- Only perform characters check when the hashes match.
- Some requirements for the hash function:
  . allow recomputation in O(1) when we slide the window.
  . low chance of collisions: same hash -> very probable match.
  . different hashes -> 100% not match

Rabin-Karp hash function:
  . hash(s) = (s[0]*p^(n-1) + s[1]*p^(n-2) + ... + s[n-1]*p^0) % q
- Calculate the hash of the first window [0..L]:
  . hash(s[0..0]) = s[0]*p^0 % q = s[0] % q
  . hash(s[0..i+1]) = (p*hash(s[0..i]) + s[i+1]) % q
- Calculate the hash of subsequent windows:
  . precompute power = p^(L-1) % q
  . hash(s[i+1..i+L]) = (p*(hash(s[i..i+L-1]) - s[i]*power) + s[i+L]) % q
  . if result < 0 -> result += q

Algorithm:
- Compute power = p^(L-1) % q
- Compute hash of `needle` and first m-element window of `haystack`
- Compare the hashes. If match, perform characters check.
  If not match after that, move to the next window.  
"""


def index_of(haystack: str, needle: str) -> int:
    n = len(haystack)
    m = len(needle)
    if n < m:
        return -1

    # Pick constants for the hash function
    p = 2
    q = int(1e9 + 7)

    # Precompute p^(m-1) % q
    power = 1
    for _ in range(1, m):
        power = (power * p) % q

    # Compute hashes for `needle` and first window of `haystack`
    needle_hash = ord(needle[0]) % q
    for i in range(1, m):
        needle_hash = (p * needle_hash + ord(needle[i])) % q

    window_hash = ord(haystack[0]) % q
    for i in range(1, m):
        window_hash = (p * window_hash + ord(haystack[i])) % q

    # Compare and slide window
    for i in range(n - m + 1):
        # Check if current window match
        if needle_hash == window_hash and _match(haystack, i, needle):
            return i

        if i < n - m:
            # Compute hash for the next window
            window_hash = (
                p * (window_hash - ord(haystack[i]) * power) + ord(haystack[i + m])
            ) % q
            if window_hash < 0:
                window_hash += q

    return -1


"""
Complexity:

1. Time complexity:
- Compute hash for `needle` and first window: O(m)
- There are n - m + 1 windows. Each iteration costs:
  . Compare characters if hashes match: O(m).
    (If the hash function is "good", this only happens once)
  . Compute hash for next window: O(1)
=> Overall: O(n + m)

2. Space complexity: O(1)
"""
