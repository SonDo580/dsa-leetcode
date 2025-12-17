"""
https://leetcode.com/problems/permutation-in-string/

Given two strings s1 and s2,
return true if s2 contains a permutation of s1, or false otherwise.

In other words, return true if one of s1's permutations is the substring of s2.
"""

# ===== Approach 1.1 =====
# ========================
"""
- For each window of size len(s1) in s2,
  check if it's a permutation of s1.
- Check permutation: check if character frequencies match.
- Update frequency dictionary when sliding window.
"""

from collections import defaultdict


def check_inclusion(s1: str, s2: str) -> bool:
    m = len(s1)
    n = len(s2)
    if m > n:
        return False

    # Find character frequency of s1 and first window
    s1_freq = _get_freq_dict(s1)
    window_freq = _get_freq_dict(s2[:m])

    for i in range(n - m):
        # Check if current window is permutation
        if window_freq == s1_freq:
            return True

        # Update character frequency for the next window
        window_freq[s2[i]] -= 1
        if window_freq[s2[i]] == 0:
            del window_freq[s2[i]]
        window_freq[s2[i + m]] += 1

    # Check if last window is permutation
    return window_freq == s1_freq


def _get_freq_dict(s: str) -> defaultdict[str, int]:
    """Produce character frequency dictionary for a string."""
    freq_dict: defaultdict[str, int] = defaultdict(int)
    for c in s:
        freq_dict[c] += 1
    return freq_dict


"""
Complexity:
- Let m = len(s1)
      n = len(s2)

1. Time complexity:
- Get character frequencies for s1 and first window: O(m)
- There are n - m + 1 windows, each iteration costs:
  . compare character frequencies: O(m)
  . update character frequencies for next window: O(1)
=> Overall: O(m + (n - m)*m) = O(m * (n - m))

2. Space complexity: O(m) for 's1_freq' and 'window_freq'
"""


# ===== Approach 1.2 =====
# ========================
"""
- Same idea but instead of using 'window_freq', 
  update character frequencies of 's1_freq'
  (track remaining frequencies).
  . reduce the character frequency when encounter.
  . increase the character frequency when remove.
- Window is permutation when all character frequencies become 0.
"""


def check_inclusion(s1: str, s2: str) -> bool:
    m = len(s1)
    n = len(s2)
    if m > n:
        return False

    # Find character frequency of s1
    freq = _get_freq_dict(s1)

    # Update frequency for the first window
    for i in range(m):
        freq[s2[i]] -= 1

    for i in range(n - m):
        # Check if current window is permutation
        if _is_permutation(freq):
            return True

        # Update character frequency for the next window
        freq[s2[i]] += 1
        freq[s2[i + m]] -= 1

    # Check if last window is permutation
    return _is_permutation(freq)


def _is_permutation(freq: defaultdict[str, int]) -> bool:
    """Window is permutation if all character frequencies become 0."""
    return all(f == 0 for f in freq.values())


"""
Complexity:

1. Time complexity:
- Get character frequencies from s1, update for the first window: O(m)
- There are n - m + 1 windows, each iteration costs:
  . check if all character frequencies become 0: O(m)
  . update character frequencies for next window: O(1)
=> Overall: O(m + (n - m)*m) = O(m * (n - m))

2. Space complexity: O(m) for 'freq'
"""

# ===== Approach 2 =====
# ======================
"""
General idea:
- Compute a hash for s1 and each window of s2
- Only perform characters check when the hashes match.
- Some requirements for the hash function:
  . allow recomputation in O(1) when we slide the window.
  . same hash -> very probable match.
  . different hashes -> 100% not match.
  
Find a hash function:
- To produce the same hash for permutations,
  only use character values, don't combine with positions.
- Let's try summing character values (a -> 1, ..., z -> 26):
  This can collide easily: 
    . hash(abc) = 1 + 2 + 3 = 6
    . hash(bbb) = 2 + 2 + 2 = 6
-> Use exponents (a -> 2^0, ..., z -> 2^25)
"""


def check_inclusion(s1: str, s2: str) -> bool:
    m = len(s1)
    n = len(s2)
    if m > n:
        return False

    # Find character frequency and hash of s1 and first window
    s1_freq: defaultdict[str, int] = defaultdict(int)
    window_freq: defaultdict[str, int] = defaultdict(int)
    s1_hash = 0
    window_hash = 0

    for i in range(m):
        s1_freq[s1[i]] += 1
        s1_hash += _char_hash(s1[i])
        window_freq[s2[i]] += 1
        window_hash += _char_hash(s2[i])

    for i in range(n - m):
        # If the hashes match, perform character frequencies check
        if window_hash == s1_hash and window_freq == s1_freq:
            return True

        # Update character frequency and hash for the next window
        window_freq[s2[i]] -= 1
        if window_freq[s2[i]] == 0:
            del window_freq[s2[i]]
        window_hash -= _char_hash(s2[i])

        window_freq[s2[i + m]] += 1
        window_hash += _char_hash(s2[i + m])

    # Check if last window is permutation
    return window_hash == s1_hash and window_freq == s1_freq


def _char_hash(c: str) -> int:
    """Compute 2^(c - 'a') as character hash."""
    return 1 << (ord(c) - ord("a"))


"""
Complexity:

1. Time complexity:
- Get character frequencies / hash for s1 and first window: O(m)
- There are n - m + 1 windows, each iteration costs:
  . compare hashes: O(1)
  . compare character frequencies: O(m)
    (if the hash function is good, this only happen once)
  . update character frequencies for next window: O(1)
=> Overall: O(n + m)

2. Space complexity: O(m) for 's1_freq' and 'window_freq'
"""
