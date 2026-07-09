"""
https://leetcode.com/problems/word-ladder/

A transformation sequence from word 'beginWord' to word 'endWord'
using a dictionary 'wordList' is a sequence of words
beginWord -> s1 -> s2 -> ... -> sk such that:

- Every adjacent pair of words differs by a single letter.
- Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
- sk == endWord

Given two words, 'beginWord' and 'endWord', and a dictionary 'wordList',
return the number of words in the shortest transformation sequence from beginWord to endWord,
or 0 if no such sequence exists.

Constraints:
. endWord.length == beginWord.length
. wordList[i].length == beginWord.length
. beginWord, endWord, and wordList[i] consist of lowercase English letters.
beginWord != endWord
. ...
"""

"""
Idea: similar to '(433).min-genetic-mutations'

- Nodes are all valid strings: {'beginWord'} | {words in 'wordList'}.
- Find neighbors of a word:
  . Loop through each character and replace it with another character.
    (lowercase English letters)
  . If the new string are in 'wordList', that's a valid mutation.
    -> Convert 'wordList' to a set for faster check.
- Perform BFS from 'beginWord'.
  When we reach 'endWord', return the minimum number of words transformation sequence.
"""

from collections import deque
import string


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    allowed_word_set: set[str] = set(word_list)

    def get_adjacent_words(word: str) -> list[str]:
        adjacent_words: list[str] = []
        for i in range(len(word)):
            for c in string.ascii_lowercase:
                if word[i] == c:
                    continue
                adjacent_word = f"{word[:i]}{c}{word[i + 1:]}"
                if adjacent_word in allowed_word_set:
                    adjacent_words.append(adjacent_word)
        return adjacent_words

    seen: set[str] = {begin_word}  # track visited words

    # (word, number of words in transformation sequence so far)
    queue: deque[(str, int)] = deque([(begin_word, 1)])

    while queue:
        word, count = queue.popleft()
        if word == end_word:
            return count

        for adjacent_word in get_adjacent_words(word):
            if adjacent_word not in seen:
                seen.add(adjacent_word)
                queue.append((adjacent_word, count + 1))

    return 0  # can not transform


"""
Complexity:
- Number of characters in each word string: n
  Number of choices for each character: m = 26
  -> Number of possible strings: m^n
- Number of valid strings (number of nodes): 
  . N = len(wordList) + (0 if begin_word in bank else 1)
      <= m^n

1. Time complexity: O(N + N*m*n^2) = O(N*m*n^2)
- Convert 'wordList' to set: O(N)
- BFS:
  - Compute neighbors for each node: O(n*(m-1)*n) = O(m*n^2)
    . Loop through n characters.
      Try (m-1) other choices for each character.
      String concatenation to compute 1 neighbor: O(n)
  - Visit all edges of each node: O(m*n) 
    . each node has at most (m-1)*n neighbors.
  -> For all nodes: O(N * (m*n^2 + m*n)) = O(N*m*n^2)

2. Space complexity: O(N + m*n)
- 'seen': O(N)
- 'allowed_word_set': O(N)
- queue: O(N') where N' < N (don't hold all nodes at once)
- neighbors: O(m*n) (each node has at most (m-1)*n neighbors)
"""
