"""
https://leetcode.com/problems/longest-word-in-dictionary/

Given an array of strings 'words' representing an English Dictionary,
return the longest word in 'words' that can be built one character
at a time by other words in 'words'.

If there is more than one possible answer,
return the longest word with the smallest lexicographical order.
If there is no answer, return the empty string.

Note that the word should be built from left to right with
each additional character being added to the end of a previous word.
"""

"""
Idea:
- Sort the words lexicographically.
- Insert words into a trie in that order.
- If a word cannot be built incrementally from a previous word
  (match all characters except the last), skip it.
  -> The trie only contains completed nodes (mark end of word), except the root.
- Initially, answer is "".
  If a word is inserted successfully and is longer than current answer,
  update current answer.
  (We need word with smallest lexicographical order, so only update when
   the later inserted word is longer)
"""


class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.completed: bool = False  # mark end of word


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> bool:
        """
        Return True if word can be built incrementally
        from a previously inserted word.
        Otherwise, don't update the trie and return False.
        """
        # must match all characters except the last
        curr = self.root
        for i in range(len(word) - 1):
            c = word[i]
            if c not in curr.children:
                return False
            curr = curr.children[c]
            assert curr.completed

        # insert the last character
        c = word[len(word) - 1]
        if c in curr.children:  # duplicate word
            assert curr.children[c].completed
            return False
        
        curr.children[c] = TrieNode()
        curr = curr.children[c]
        curr.completed = True
        return True


def longest_word(words: list[str]) -> str:
    ans = ""
    trie = Trie()
    words.sort()

    for word in words:
        if trie.insert(word) and len(word) > len(ans):
            ans = word
    return ans


"""
Complexity:
- Let n = len(words)
      l = len(words[i])

1. Time complexity: O(n*l*log(n))
- Sort 'words': O(n*l*log(n))   (string comparison takes O(l))
- Insert all words into trie: O(n*l)

2. Space complexity: O(n*l)
- Sort 'words': O(n) (timsort)
- trie: O(n*l) 
"""
