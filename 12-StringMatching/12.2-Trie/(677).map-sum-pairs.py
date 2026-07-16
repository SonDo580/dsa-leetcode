"""
https://leetcode.com/problems/map-sum-pairs/

Design a map that allows you to do the following:
- Maps a string key to a given value.
- Returns the sum of the values that have a key with a prefix equal to a given string.

Implement the MapSum class:
- MapSum() Initializes the MapSum object.
- void insert(String key, int val) Inserts the key-val pair into the map.
  If the key already existed, the original key-value pair will be overridden to the new one.
- int sum(string prefix) Returns the sum of all the pairs' value whose key starts with the prefix.
"""


# === Approach 1: Hashmap ===
class MapSum:
    def __init__(self):
        self.pairs: dict[str, int] = {}

    def insert(self, key: str, val: int) -> None:
        self.pairs[key] = val

    def sum(self, prefix: str) -> int:
        total = 0
        for k, v in self.pairs.items():
            if k.startswith(prefix):
                total += v
        return total


"""
Complexity:
- Let n = number of KV pairs inserted
      k = len(key)
      p = len(prefix)

1. Time complexity:
- insert: O(1)
- sum: O(n*p)
  . iterate through n entries
  . prefix comparison: O(p)

2. Space complexity: O(n*k) for 'pairs' dict
"""


# === Approach 2.1: Trie + DFS/BFS ===
"""
- Insert the string keys into a trie.
  Store value at the node that completes the string key.
  (overwrite existing value).
- Find sum of values with key prefix:
  . Match the prefix
  . Perform traversal from reached node to find all nodes with values.
    Return sum of those values.
"""


class TrieNode1:
    def __init__(self):
        self.children: dict[str, TrieNode1] = {}
        self.val: int | None = None


class Trie1:
    def __init__(self):
        self.root = TrieNode1()

    def insert(self, key: str, val: int) -> None:
        curr = self.root
        for c in key:
            if c not in curr.children:
                curr.children[c] = TrieNode1()
            curr = curr.children[c]
        curr.val = val

    def sum(self, prefix: str) -> int:
        # match prefix
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return 0
            curr = curr.children[c]

        # DFS to sum values of nodes reachable from curr
        stack: list[TrieNode1] = [curr]
        total = 0
        while stack:
            node = stack.pop()
            if node.val is not None:
                total += node.val
            for child in node.children.values():
                stack.append(child)

        return total


class MapSum:
    def __init__(self):
        self.trie = Trie1()

    def insert(self, key: str, val: int) -> None:
        self.trie.insert(key, val)

    def sum(self, prefix: str) -> int:
        return self.trie.sum(prefix)


"""
Complexity:
- Let n = number of KV pairs inserted
      k = len(key)
      p = len(prefix)

1. Time complexity:
- insert: O(k)
- sum: O(p + n*k)
  . match prefix: O(p)
  . DFS from reached node: O(n*k)

2. Space complexity: O(n*k)
- trie: O(n*k)
- 'sum' specific:
  . stack: O(n*k)
"""


# === Approach 2.2: Store precomputed result at trie node ===
"""
- Each trie node will store sum of values for keys sharing a prefix.
- Insert: 
  . Add value to result of every encountered node.
  . If overwrite value of a completed node, traverse up to root 
    and subtract the old value from result of every node.
    -> the trie nodes need to track parent.
- Sum:
  . Match the prefix.
  . Return precomputed result at reached node.
"""

from __future__ import annotations


class TrieNode2:
    def __init__(self, parent: TrieNode2 | None = None):
        self.parent = parent
        self.children: dict[str, TrieNode2] = {}
        self.val: int | None = None  # only set val at end of key

        # sum of values for keys sharing prefix path (from root to current node)
        self.total: int = 0


class Trie2:
    def __init__(self):
        self.root = TrieNode2()

    def insert(self, key: str, val: int) -> None:
        curr = self.root
        for c in key:
            if c not in curr.children:
                curr.children[c] = TrieNode2(parent=curr)
            curr = curr.children[c]
            curr.total += val

        old_val = curr.val
        curr.val = val
        if old_val is not None:
            while curr != self.root:
                curr.total -= old_val
                curr = curr.parent

    def sum(self, prefix: str) -> int:
        # match prefix
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return 0
            curr = curr.children[c]

        # return precomputed result
        return curr.total


class MapSum:
    def __init__(self):
        self.trie = Trie2()

    def insert(self, key: str, val: int) -> None:
        self.trie.insert(key, val)

    def sum(self, prefix: str) -> int:
        return self.trie.sum(prefix)


"""
Complexity:
- Let n = number of KV pairs inserted
      k = len(key)
      p = len(prefix)

1. Time complexity:
- insert: O(k)
  . insert KV: O(k)
  . (may) traverse back to root: O(k)
- sum: O(p)
  . match prefix: O(p)
  . return precomputed result: O(1)

2. Space complexity: O(n*k) for trie
"""
