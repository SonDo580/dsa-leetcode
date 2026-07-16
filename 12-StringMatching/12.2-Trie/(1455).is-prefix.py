"""
https://leetcode.com/problems/check-if-a-word-occurs-as-a-prefix-of-any-word-in-a-sentence/

Given a sentence that consists of some words separated by a single space,
and a searchWord, check if searchWord is a prefix of any word in sentence.

Return the index of the word in sentence (1-indexed)
where searchWord is a prefix of this word.
If searchWord is a prefix of more than one word,
return the index of the first word (minimum index).
If there is no such word return -1.

A prefix of a string s is any leading contiguous substring of s.
"""

"""
Idea:
- Break sentence into words and insert into a trie.
- Optimize: 
  . Don't break sentence into words explicitly.
    Insert characters sequentially into the trie.
  . When a space encountered, skip it, increment word index counter,
    and rewind to the root to insert next word.
- Record word indices that share prefix at each trie node.
  . Only need index of the 1st word in each group.
- Query: Match searchWord and return the index recorded at reached node.
"""


class TrieNode:
    def __init__(self, first_word_idx: int):
        self.children: dict[str, TrieNode] = {}
        self.first_word_idx = first_word_idx


class Trie:
    def __init__(self):
        self.root = TrieNode(-1)  # dummy first_word_idx

    def insert_sentence(self, sentence: str) -> None:
        """Insert words in space-separated sentence into the trie."""
        word_idx = 1
        curr = self.root

        for c in sentence:
            if c == " ":
                word_idx += 1
                curr = self.root  # go back to root to match next word
                continue

            if c not in curr.children:
                curr.children[c] = TrieNode(word_idx)
            curr = curr.children[c]

    def is_prefix_of(self, search_word: str) -> int:
        """
        Return index of the 1st word where search_word is its prefix.
        Return -1 if search_word is not prefix of any word.
        """
        curr = self.root
        for c in search_word:
            if c not in curr.children:
                return -1
            curr = curr.children[c]
        return curr.first_word_idx


def is_prefix_of_word(sentence: str, search_word: str) -> int:
    trie = Trie()
    trie.insert_sentence(sentence)
    return trie.is_prefix_of(search_word)


"""
Complexity:
- Let n = len(sentence)
      m = len(search_word)

1. Time complexity: O(n + m)
- Build trie: O(n)
- Check prefix: O(m)

2. Space complexity: O(n) for the trie
"""
