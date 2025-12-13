"""
(208) https://leetcode.com/problems/implement-trie-prefix-tree/

A trie (pronounced as "try") or prefix tree is a tree data structure
used to efficiently store and retrieve keys in a dataset of strings.
There are various applications of this data structure,
such as autocomplete and spellchecker.

Implement the Trie class:
Trie() Initializes the trie object.
void insert(String word) Inserts the string word into the trie.
boolean search(String word) Returns true if the string word is in the trie (i.e., was inserted before), and false otherwise.
boolean startsWith(String prefix) Returns true if there is a previously inserted string word that has the prefix prefix, and false otherwise.

Constraints:
1 <= word.length, prefix.length <= 2000
word and prefix consist only of lowercase English letters.
At most 3 * 10^4 calls in total will be made to insert, search, and startsWith.
"""

"""
Trie structure:
- The root represent the empty string "".
- An edge represents the next character in a string. 
- A node can have optional data.
  (In this problem we don't need any data).
- If the path from root to a node represents a full word,
  add a marker for that node.
"""

# ========== Option 1 ==========
# ==============================
"""
Represent Trie nodes as hash maps.
Use this if don't need to store data at each node. 
"""

TTrieNode = dict[str, "TTrieNode"]
END = "END"  # mark end of word


class Trie:
    def __init__(self):
        self.root: TTrieNode = {}

    def insert(self, word: str) -> None:
        current = self.root
        for c in word:
            if c not in current:
                current[c] = {}
            current = current[c]
        current[END] = {}

    def search(self, word: str) -> bool:
        current = self.root
        for c in word:
            if c not in current:
                return False
            current = current[c]
        return END in current

    def startsWith(self, prefix: str) -> bool:
        current = self.root
        for c in prefix:
            if c not in current:
                return False
            current = current[c]
        return True


# ========== Option 2 ==========
# ==============================
"""
Represent Trie nodes as objects.
Use this if need to store data at each node. 
"""


class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.completed: bool = False  # mark full word
        self.data = None  # don't need data in this problem


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        current = self.root
        for c in word:
            if c not in current.children:
                current.children[c] = TrieNode()
            current = current.children[c]
        current.completed = True

    def search(self, word: str) -> bool:
        current = self.root
        for c in word:
            if c not in current.children:
                return False
            current = current.children[c]
        return current.completed

    def startsWith(self, prefix: str) -> bool:
        current = self.root
        for c in prefix:
            if c not in current.children:
                return False
            current = current.children[c]
        return True


"""
Complexity:
- Let k = average input length
      n = number of words inserted

1. Time complexity:
- insert: O(k) 
- search: O(k)
- startsWith: O(k)

2. Space complexity: O(n * k)
(worst case: the words don't share prefix)
"""
