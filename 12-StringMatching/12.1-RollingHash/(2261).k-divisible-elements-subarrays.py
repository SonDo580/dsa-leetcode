"""
https://leetcode.com/problems/k-divisible-elements-subarrays/

Given an integer array 'nums' and two integers k and p,
return the number of distinct sub-arrays,
which have at most k elements that are divisible by p.

Two arrays 'nums1' and 'nums2' are said to be distinct if:
- They are of different lengths, or
- There exists at least one index i where nums1[i] != nums2[i].

A sub-array is a non-empty contiguous sequence of elements in an array.

Follow up: Can you solve this problem in O(n^2) time complexity?
"""

"""
Idea:
- Use sliding window to collect sub-arrays
  . Window constraint: at most k elements divisible by p.
  . When window [left..right] is valid, all windows [i..right] are valid
    (i in range [left..right]).
- Avoid duplicates: Need a way to hash the sub-array
 . Method 1: convert sub-array to tuple and add to set.
 . Method 2: rolling hash
 . Method 3: trie for suffix matching
"""


# === Method 1: Avoid duplicates with set of tuples ===
def count_distinct(nums: list[int], k: int, p: int) -> int:
    divisible_by_p_cnt = 0  # number of elements divisible by p in current window
    seen: set[tuple] = set()  # valid windows encountered
    ans = 0  # number of distinct valid windows

    left = 0
    for right in range(len(nums)):
        if nums[right] % p == 0:
            divisible_by_p_cnt += 1
        while divisible_by_p_cnt > k:
            if nums[left] % p == 0:
                divisible_by_p_cnt -= 1
            left += 1

        # check all valid windows that end at 'right'
        for i in range(left, right + 1):
            sub_arr_tup = tuple(nums[i : right + 1])
            if sub_arr_tup not in seen:
                seen.add(sub_arr_tup)
                ans += 1

    return ans


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n^3)
- 'right' moves: O(n)
- 'left' moves: O(n) in total 
- slice 'nums', convert to tuple, tuple hashing: O(L)
  -> for all valid windows that ends at a fixed 'right': 
     . sum(O(L) for L in [1..right-left+1]) = O(right^2)
       . worst case: k >= n -> 'left' stays at 0
  -> across all 'right' values: 
     . sum(O(right^2) for right in [0..n-1]) = O(n^3)

2. Space complexity: O(n^3) for 'seen'
- Worst case: all windows of 'nums' is valid.
- Windows of each length:
  . length n: 1 window
  . length n-1: 2 windows
  . length L: n-L+1 windows
  . ...
  . length 1: n windows
-> space = sum(L_cnt * L for L in [1..n])
         = sum((n-L+1)*L for L in [1..n])
         = (n+1)*sum(L for L in [1..n]) - sum(L^2 for L in [1..n])
         = (n+1)*n*(n+1)/2 - n*(n+1)*(2n+1)/6
         = O(n^3)
"""


# === Method 2: Avoid duplicates with rolling hash ===
"""
- Use rolling hash to recalculate hash value quickly when elements 
  enter and leave the window. 
- hash value not found -> the window hasn't been encountered.
- hash value found -> compare elements with all windows in the same bucket.

Rabin-Karp hash function:
. hash(s) = (s[0]*p^(n-1) + s[1]*p^(n-2) + ... + s[n-1]*p^0) % q
  . p is a small base (prime number, commonly 31 or 37)
    -> pick 2 for easy power calculation (by shifting bits)
  . q is a larger prime number to avoid overflow and reduce collisions
    -> pick 1e9 + 7
- Calculate the hash of window [0..L] (fixed start):
  . hash(s[0..i]) = (s[0]*p^(i-1) + s[1]*p^(n-2) + ... + s[i]*p^0) % q
  . hash(s[0..i+1]) = (s[0]*p^i + s[1]*p^(n-1) + ... + s[i+1]*p^0) % q
                    = (p*hash(s[0..i]) + s[i+1]) % q
  . base case: hash(s[0..0]) = s[0]*p^0 % q = s[0] % q

Apply to our problem:
- Check all valid windows that end at 'right'
  -> Iterate in [right..left] order to build the hash incrementally.
"""


def _window_eq(nums: list[int], l1: int, r1: int, l2: int, r2: int) -> bool:
    """Return true if nums[l1:r1] == nums[l2:r2]"""
    n = len(nums)
    assert (0 <= l1 <= r1 < n) and (0 <= l2 <= r2 < n)

    if r1 - l1 != r2 - l2:  # size mismatch
        return False

    size = r1 - l1 + 1
    for j in range(size):
        if nums[l1 + j] != nums[l2 + j]:
            return False

    return True


def count_distinct(nums: list[int], k: int, p: int) -> int:
    divisible_by_p_cnt = 0  # number of elements divisible by p in current window
    ans = 0  # number of distinct valid windows

    # group valid windows by hash value (collisions)
    # store left and right bounds instead of the whole array.
    seen: dict[int, list[tuple[int, int]]] = {}

    # pick constants for rolling hash function
    base = 2
    mod = 1_000_000_007

    left = 0
    for right in range(len(nums)):
        if nums[right] % p == 0:
            divisible_by_p_cnt += 1
        while divisible_by_p_cnt > k:
            if nums[left] % p == 0:
                divisible_by_p_cnt -= 1
            left += 1

        # check all valid windows that end at 'right'
        # (iterate in reverse order to build the hash incrementally)
        hash = nums[right] % mod
        for i in range(right, left - 1, -1):
            if hash not in seen:
                ans += 1
                seen[hash] = [(i, right)]
            else:
                found = False
                for l, r in seen[hash]:  # compare with windows in the same bucket
                    if _window_eq(nums, l1=i, r1=right, l2=l, r2=r):
                        found = True
                        break
                if not found:
                    seen[hash].append((i, right))
                    ans += 1

            if i > left:
                hash = (base * hash + nums[i - 1]) % mod

    return ans


"""
Complexity:
- Let n = len(nums)

1. Time complexity: still O(n^3)
(but in case hash value is new, we instantly know current window hasn't been encountered)

- 'right' moves O(n) times.
- 'left' moves O(n) times.
- for each window that ends at a given 'right':
  . if the hash function is good, each bucket has 1 window
    -> compare elements of current window with window in the bucket: O(L)
  -> work for all windows that ends at a given 'right':
     . sum(O(L) for L in [1..right-left+1]) = O(right^2)
       . worst case: k >= n -> 'left' stays at 0
  -> across all 'right' values:
     . sum(O(right^2) for right in [0..n-1]) = O(n^3)

2. Space complexity: O(n^2 for 'seen')
- Worst case: all windows of 'nums' is valid.
- Windows of each length:
  . length n: 1 window
  . length n-1: 2 windows
  . length L: n-L+1 windows
  . ...
  . length 1: n windows
- But we don't store the whole window, just the left and right bounds
  -> space = 1 + 2 + ... + n = n*(n+1)/2 = O(n^2)
"""


# === Method 3: Avoid duplicates with trie ===
"""
- Check all valid windows that end at 'right'
  -> Build a trie for suffix matching ('right' is in root.children)
- All trie nodes are completed, except root
  (a path from any node to root forms a valid window)
  -> Don't need to track 'completed' explicitly.
- For each valid window:
  . Iterate in [right..left] order.
  . If matching nums[i] reaches a completed trie node,
    the window [i..right] already exists.
  . Otherwise, insert a new trie node and
    increment number of distinct valid windows.
- Note: 
"""


class TrieNode:
    def __init__(self):
        self.children: dict[int, TrieNode] = {}  # numeric keys


class Trie:
    """Trie for suffix matching"""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, nums: list[int], left: int, right: int) -> int:
        """Insert/Match nums[left..right] in reverse order. Return number of inserted nodes."""
        curr = self.root
        inserted_cnt = 0
        for i in range(right, left - 1, -1):
            num = nums[i]
            if num not in curr.children:
                curr.children[num] = TrieNode()
                inserted_cnt += 1
            curr = curr.children[num]
        return inserted_cnt


def count_distinct(nums: list[int], k: int, p: int) -> int:
    divisible_by_p_cnt = 0  # number of elements divisible by p in current window
    trie = Trie()
    ans = 0  # number of distinct valid windows

    left = 0
    for right in range(len(nums)):
        if nums[right] % p == 0:
            divisible_by_p_cnt += 1
        while divisible_by_p_cnt > k:
            if nums[left] % p == 0:
                divisible_by_p_cnt -= 1
            left += 1

        # check all valid windows that end at 'right'
        ans += trie.insert(nums, left, right)

    return ans


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n^2)
- 'right' moves O(n) times.
- 'left' moves O(n) times.
- check all valid windows that ends at a given 'right': O(right)
  (worst case: k >= n -> 'left' stays at 0)
  -> for all values of 'right':
     . sum(O(right) for right in [0..n-1]) = O(n^2)

2. Space complexity: O(n) for trie
"""