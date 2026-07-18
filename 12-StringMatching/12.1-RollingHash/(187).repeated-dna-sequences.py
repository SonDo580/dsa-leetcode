"""
https://leetcode.com/problems/repeated-dna-sequences/

The DNA sequence is composed of a series of nucleotides
abbreviated as 'A', 'C', 'G', and 'T'.

For example, "ACGAATTCCG" is a DNA sequence.
When studying DNA, it is useful to identify repeated sequences within the DNA.

Given a string s that represents a DNA sequence,
return all the 10-letter-long sequences (substrings)
that occur more than once in a DNA molecule.
You may return the answer in any order.
"""

"""
Idea:
- Slide a window of size 10 across the sequence.
- Add a substring to answer if it has been encountered once.
- Check occurrence:
  . method 1: map of string frequencies
  . method 2: rolling hash
  . method 3: trie
"""

# === Approach 1: Map of string frequencies ===
"""
- Use a dict to record number of occurrences for each substring.
- After incrementing frequency, add key with frequency 2 to result. 
"""

from collections import defaultdict


def find_repeated_dna_sequences(s: str) -> list[str]:
    n = len(s)
    L = 10  # fixed window size

    ans: list[str] = []
    freq: defaultdict[str, int] = defaultdict(int)
    for i in range(n - L + 1):
        substr = s[i : i + L]
        freq[substr] += 1
        if freq[substr] == 2:
            # add to answer once
            ans.append(substr)

    return ans


"""
Complexity:
- n = len(s), L = 10 (fixed window size)

1. Time complexity: O((n-L)*L)
- Iterate through n-L+1 valid windows. Each costs:
  . string slicing: O(L)
  . calculate hash for string: O(L)

2. Space complexity: O((n-L)*L)
- 'freq' dict: O((n-L)*L)
  . max number of entries: n-L+1
  . space for each key: O(L)
  . space for each value: O(1)
"""


# === Approach 2: Rolling hash ===
"""
- Calculate hash value of each substring with a rolling hash function
  (allow recalculating hash value quickly when sliding window).
- Use a dict to record list of substrings with the same hash value.
  . only store left and right bounds, don't store the whole substring.
- For each substring:
  . hash value not found -> definitely a new substring.
  . hash value found:
    . compare characters with unique substrings in the same bucket.
      (only 1 item if the hash function is good).
    . if match a previous unique substring, add current substring to result.
- To avoid adding duplicate substring, 
  track which entries in a bucket has been recorded
  . main dict: hash -> list(substr1_bounds, substr2_bounds)
    recorded dict: hash -> set(0)
    -> substr1 has been added to result

=== Hash function ===
- Window size = 10
  4 possible values for each position
  -> total possibility: 4^10 = 2^20
- Using 20 bits, we can represent any valid window without collisions:
  . each window map to exactly 1 20-bit integer.
  . 2 bits represent 1 letter:
    . A = 00 (0), C = 01 (1), G = 10 (2), T = 11 (3)
- Calculate hash value for the 1st 10-letter window:
  . OR(val(s[i]) << 2*i for i in [0..9])
- Update hash value when sliding window:    
  . remove leftmost letter: 
    . shift right by 2 -> 2 MSBs (18 and 19) are now 0
      (logical right shift)
  . append new letter:
    . shift left val(new_letter) by 18 
      then OR with current hash value.

=== Improved algorithm ===
- Since the hash function guarantees no collisions,
  if 2 hashes match, 2 substrings are the same.
- Use a dict to record frequency of each hash value.
  Each hash value is guaranteed to represent only 1 string. 
- If frequency == 2 after incrementing frequency of a hash value,
  slice the string and add to result. 
"""

from collections import defaultdict


def find_repeated_dna_sequences(s: str) -> list[str]:
    n = len(s)
    L = 10  # fixed window size
    if n < L:
        return []

    letter_hash: dict[str, int] = {"A": 0, "C": 1, "G": 2, "T": 3}

    ans: list[str] = []

    # frequency of hash value (each corresponds to 1 unique substring)
    freq: defaultdict[int, int] = defaultdict(int)

    # calculate hash value for 1st window
    hash = 0
    for i in range(L):
        hash |= letter_hash[s[i]] << (2 * i)

    for i in range(n - L + 1):
        freq[hash] += 1
        if freq[hash] == 2:
            ans.append(s[i : i + L])

        # calculate hash for next window
        if i < n - L:
            hash >>= 2  # remove leftmost letter
            hash |= letter_hash[s[i + L]] << (2 * (L - 1))  # append next letter

    return ans


"""
Complexity:

1. Time complexity: O(L + (n-L)*L) = O(n-L)*L)
- Calculate hash for the 1st window: O(L)
- Slide through n-L remaining windows:
  . Recalculate hash for each new window: O(1)
  . String slicing for 2nd window of each group: O(L)

2. Space complexity: O(n-L)
- 'letter_hash' dict: O(4) = O(1)
- 'freq' dict: O(n-L+1) = O(n-L)
"""

# === Approach 3: Trie ===
"""
- Insert substrings into a trie.
  Completed nodes denote end of a full substring.
- If the substring matches a completed path,
  it has been encountered before 
  -> record it.
- Don't record if a substring has been recorded
  -> add 'recorded' state to completed nodes.
"""


class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.completed: bool = False
        self.recorded: bool = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, s: str, left: int, right: int, ans: list[str]) -> None:
        """
        Insert s[left..right] into trie.
        Add to answer if it matches a completed path that hasn't been recorded.
        """
        curr = self.root
        for i in range(left, right + 1):
            c = s[i]
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]

        if curr.completed and not curr.recorded:
            curr.recorded = True
            ans.append(s[left : right + 1])
            return
        curr.completed = True


def find_repeated_dna_sequences(s: str) -> list[str]:
    n = len(s)
    L = 10  # fixed window size

    ans: list[str] = []
    trie = Trie()

    for i in range(n - L + 1):
        # insert substring into trie + populate 'ans'
        trie.insert(s, i, i + L - 1, ans)

    return ans


"""
Complexity:

1. Time complexity: O(n-L)*L)
- There are (n-L+1) L-letter substrings.
- Insert 1 substring into trie: O(L)
  -> Insert all into trie: O(n-L)*L)
- String slicing for 2nd window of each group: O(L)
  -> total: O((n-L)*L)

2. Space complexity: O(n-L)*L) for trie
"""
