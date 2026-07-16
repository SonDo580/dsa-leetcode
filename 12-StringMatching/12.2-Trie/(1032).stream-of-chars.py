"""
https://leetcode.com/problems/stream-of-characters/

Design an algorithm that accepts a stream of characters and checks if
a suffix of these characters is a string of a given array of strings words.

For example, if words = ["abc", "xyz"] and the stream added the 4 characters
(one by one) 'a', 'x', 'y', and 'z', your algorithm should detect that
the suffix "xyz" of the characters "axyz" matches "xyz" from words.

Implement the StreamChecker class:
- StreamChecker(String[] words):
  . Initializes the object with the strings array words.
- boolean query(char letter):
  . Accepts a new character from the stream and returns true if
    any non-empty suffix from the stream forms a word that is in words.
"""

# === Approach 1: trie for suffix match ===
"""
- Insert characters of each word in reverse order
  . Last letter is in root.children.
  . Mark completed node after the 1st letter.
- When query, match the characters in stream in reverse order.
- The StreamChecker should maintain a queue of received letters 
  with size = max word length.
"""

from typing import Iterable
from collections import deque


class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.completed: bool = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert characters of word in reverse order."""
        curr = self.root
        for c in reversed(word):
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.completed = True

    def match_suffix(self, letters: Iterable[str]) -> bool:
        """Return True if rear-end of letters is suffix of any inserted word."""
        curr = self.root
        for c in reversed(letters):
            if c not in curr.children:
                return False
            curr = curr.children[c]
            if curr.completed:
                return True
        return False


class StreamChecker:
    def __init__(self, words: list[str]):
        self.last_letters: deque[str] = deque()
        self.trie = Trie()

        self.max_word_len = -1
        for word in words:
            self.trie.insert(word)
            if len(word) > self.max_word_len:
                self.max_word_len = len(word)

    def query(self, letter: str) -> bool:
        self.last_letters.append(letter)
        if len(self.last_letters) > self.max_word_len:
            self.last_letters.popleft()
        return self.trie.match_suffix(self.last_letters)


"""
Complexity:
- Let n = len(words)
      l = len(words[i])

1. Time complexity:
- init: O(n*l)
- query: O(l)

2. Space complexity: O(n*l)
- 'last_letters' queue: O(l)
- trie: O(n*l)
"""


# === Approach 2: trie for prefix match + incremental match ===
"""
- Insert all words into a trie. A completed node ends a full word.
- query(letter):
  . Each new letter can possibly be:
    . the first letter of a full word 
      -> traverse from root.
    . the next letter in some words we are exploring
      -> extend the paths from matching previous letter
         (traverse from last reached nodes)
  . If by matching current letter, we can reach a completed node, 
    the result for current query is True.
    Explore remaining paths before returning.
- Implementation notes:
  . Keep track of last reached nodes from matching previous letter.
  . Reassign new reached nodes instead of modifying existing structure
"""


class TrieNode2:
    def __init__(self):
        self.children: dict[str, TrieNode2] = {}
        self.completed: bool = False


class Trie2:
    def __init__(self):
        self.root = TrieNode2()

        # reached nodes from matching previous letters
        self.reached_nodes: set[TrieNode2] = set()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode2()
            curr = curr.children[c]
        curr.completed = True

    def match_suffix(self, letter: str) -> bool:
        new_reached_nodes: set[TrieNode2] = set()
        matched: bool = False

        # try starting from the root
        # plus continuing paths from matching previous letter
        self.reached_nodes.add(self.root)
        for node in self.reached_nodes:
            child = node.children.get(letter)
            if not child:
                continue
            new_reached_nodes.add(child)
            if child.completed:
                matched = True
                # explore remaining paths, don't break

        # update last reached nodes
        self.reached_nodes = new_reached_nodes

        return matched


class StreamChecker:
    def __init__(self, words: list[str]):
        self.trie = Trie2()
        for word in words:
            self.trie.insert(word)

    def query(self, letter: str) -> bool:
        return self.trie.match_suffix(letter)


"""
Complexity:
- Let n = len(words)
      l = len(words[i])

1. Time complexity:
- init: O(n*l)
- query: O(n) (continue from at most n word prefixes)

2. Space complexity: O(n*l)
- trie: O(n*l)
- reached_nodes: O(n) (reach at most 1 node in each of n branches)
"""
