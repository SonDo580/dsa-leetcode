# A pangram is a sentence where every letter of the English alphabet
# appears at least once.

# Given a string sentence containing only lowercase English letters,
# return true if sentence is a pangram, or false otherwise.

# Example 1:
# Input: sentence = "thequickbrownfoxjumpsoverthelazydog"
# Output: true
# Explanation: sentence contains at least one of every letter of the English alphabet.

# Example 2:
# Input: sentence = "leetcode"
# Output: false

# Constraints:
# 1 <= sentence.length <= 1000
# sentence consists of lowercase English letters.


def is_pangram(sentence: str) -> bool:
    if len(sentence) < 26:
        return False

    char_set = set()
    for char in sentence:
        char_set.add(char)

        if len(char_set) == 26:
            return True

    return len(char_set) == 26 
    
