# A transformation sequence from word 'beginWord' to word 'endWord'
# using a dictionary 'wordList' is a sequence of words
# beginWord -> s1 -> s2 -> ... -> sk such that:
#
# - Every adjacent pair of words differs by a single letter.
# - Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
# - sk == endWord
#
# Given two words, 'beginWord' and 'endWord', and a dictionary 'wordList',
# return the number of words in the shortest transformation sequence from beginWord to endWord,
# or 0 if no such sequence exists.

# Example 1:
# Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
# Output: 5
# Explanation: One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> cog", which is 5 words long.

# Example 2:
# Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
# Output: 0
# Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.

# Constraints:
# 1 <= beginWord.length <= 10
# endWord.length == beginWord.length
# 1 <= wordList.length <= 5000
# wordList[i].length == beginWord.length
# beginWord, endWord, and wordList[i] consist of lowercase English letters.
# beginWord != endWord
# All the words in wordList are unique.


# ===== Analysis =====
# (similar to problem 5.6/01 - Minimum Genetic Mutation)

from collections import deque
import string


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    allowed_word_set: set[str] = set(word_list)

    def get_adjacent_words(word: str) -> list[str]:
        adjacent_words: list[str] = []
        for i in range(len(word)):
            for c in string.ascii_lowercase:
                if word[i] != c:
                    adjacent_word = f"{word[:i]}{c}{word[i + 1:]}"
                    if adjacent_word in allowed_word_set:
                        adjacent_words.append(adjacent_word)
        return adjacent_words

    seen: set[str] = {begin_word}  # track visited words
    queue: deque[(str, int)] = deque(
        [(begin_word, 1)]
    )  # (word, number of words so far)

    while queue:
        word, count = queue.popleft()

        if word == end_word:
            return count

        for adjacent_word in get_adjacent_words(word):
            if adjacent_word not in seen:
                seen.add(adjacent_word)
                queue.append((adjacent_word, count + 1))

    return 0  # can not transform
