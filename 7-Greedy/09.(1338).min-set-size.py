"""
https://leetcode.com/problems/reduce-array-size-to-the-half/

You are given an integer array 'arr'.
You can choose a set of integers and remove all the occurrences of these integers in the array.
Return the minimum size of the set so that at least half of the integers of the array are removed.
"""

"""
Analysis:
- The goal is to remove as much integers as possible each time.
-> Just remove all occurrences of the most frequent integer at any step.

Implementation:
- Build a hash map to store frequency of each integer.
- Sort the entries by frequency in descending order.
- Loop through entries and remove 'frequency' items at each step.
- Stop when removed set size >= n / 2.
"""


def min_set_size(arr: list[int]) -> int:
    frequency_dict: dict[int, int] = {}
    for num in arr:
        if num not in frequency_dict:
            frequency_dict[num] = 0
        frequency_dict[num] += 1

    frequencies = sorted(frequency_dict.values(), reverse=True)

    removed = 0  # number of items removed
    set_size = 0  # number of unique items removed
    half = len(arr) / 2
    for frequency in frequencies:
        removed += frequency
        set_size += 1
        if removed >= half:
            break

    return set_size


"""
Complexity:
(worst case when all integers are unique)
- Let n = len(arr)

1. Time complexity:
- build frequency dict: O(n)
- produce sorted frequencies: O(n*log(n))
- iterate through frequencies: O(n)
=> Overall: O(n*log(n))

2. Space complexity: O(n)
- 'frequency_dict': O(n)
- sorted frequencies: O(n)
"""


# === Another approach: use max heap ===
"""
- Still collect frequencies of each integers 
- Add all frequencies to a max heap.
- At each step, pick the largest frequency from the max heap.
- Note: With heapq, simulate a max heap by negating the value.
"""

import heapq


def min_set_size(arr: list[int]) -> int:
    frequency_dict: dict[int, int] = {}
    for num in arr:
        if num not in frequency_dict:
            frequency_dict[num] = 0
        frequency_dict[num] += 1

    frequencies = [-f for f in frequency_dict.values()]
    heapq.heapify(frequencies)

    removed = 0  # number of items removed
    set_size = 0  # number of unique items removed
    half = len(arr) / 2
    while removed < half:
        max_f = -heapq.heappop(frequencies)
        removed += max_f
        set_size += 1

    return set_size


"""
Complexity:
(worst case when all integers are unique)

1. Time complexity:
- build frequency dict: O(n)
- generate frequencies list: O(n)
- heapify 'frequencies': O(n)
- remove half of the items: O(n*log(n)) (heappop takes O(log(n)))
=> Overall: O(n*log(n))

2. Space complexity: O(n)
- 'frequency_dict': O(n)
- 'frequencies' heap: O(n)
"""
