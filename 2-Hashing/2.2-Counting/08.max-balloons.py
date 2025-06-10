# Given a string text, you want to use the characters of text to form as many instances of the word "balloon" as possible.
# You can use each character in text at most once. Return the maximum number of instances that can be formed.

# Example 1:
# Input: text = "nlaebolko"
# Output: 1

# Example 2:
# Input: text = "loonbalxballpoon"
# Output: 2

# Example 3:
# Input: text = "leetcode"
# Output: 0

# Constraints:
# 1 <= text.length <= 10^4
# text consists of lower case English letters only.

# ===== Strategy =====
# - Find the frequency of each unique character in "balloon" and text
# - Consider each unique character in "balloon"
#   + If text doesn't have that character, or the frequency is less than in balloon
#     -> Return 0
#   + Calculate how many times that character can be built in text.
#     Use floor division.
# - The total number of "balloon" is the minimum of those values.

from collections import defaultdict


def max_number_of_balloons(text: str) -> int:
    balloon_frequency_dict: defaultdict[int, int] = defaultdict(int)
    for c in "balloon":
        balloon_frequency_dict[c] += 1

    text_frequency_dict: defaultdict[int, int] = defaultdict(int)
    for c in text:
        text_frequency_dict[c] += 1

    num_instances = float("inf")
    for c, frequency in balloon_frequency_dict.items():
        if c not in text_frequency_dict or text_frequency_dict[c] < frequency:
            return 0
        num_instances = min(text_frequency_dict[c] // frequency, num_instances)

    return num_instances

# ===== Complexity =====
# 1. Time complexity:
# - build text frequency dict: O(n)
# - build "ballon" frequency dict and loop through it: O(1)
# => Overall: O(n)
#
# 2. Space complexity:
# - text frequency dict: O(n)
# - "balloon" frequency dict: O(1)
# => Overall: O(n)
