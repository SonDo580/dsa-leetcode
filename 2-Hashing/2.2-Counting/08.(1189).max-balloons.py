"""
https://leetcode.com/problems/maximum-number-of-balloons/

Given a string 'text', you want to use the characters of text
to form as many instances of the word "balloon" as possible.
You can use each character in text at most once.
Return the maximum number of instances that can be formed.
"""

"""
Idea: 
- Find the frequency of each unique character in "balloon" and 'text'
- Consider each unique character in "balloon"
  + If text doesn't have that character, or the frequency is less than in 'balloon'
    -> Return 0
  + Calculate how many times that character can be built in 'text':
    with floor division of frequencies.
    The total number of "balloon" is the minimum of those values.
"""

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


"""
Complexity:
- Let n = len(text)

1. Time complexity: O(n)
- build text frequency dict: O(n)
- build "ballon" frequency dict and loop through it: O(1)

2. Space complexity: O(n)
- text frequency dict: O(n)
- "balloon" frequency dict: O(1)
"""
