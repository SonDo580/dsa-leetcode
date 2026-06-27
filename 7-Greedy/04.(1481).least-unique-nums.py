"""
https://leetcode.com/problems/least-number-of-unique-integers-after-k-removals/

Given an array of integers 'arr' and an integer k.
Find the least number of unique integers after removing exactly k elements.
"""

"""
Analysis:
- The number of unique integers is reduced only if we remove all of an element
  -> We should remove the element with lowest frequency at any step

Implementation:
- Use a hashmap to track frequency of each element.
- Sort the frequencies in descending order.
- At each step, pick the smallest frequency f.
  If f <= k, decrease k by f (remove f elements).
- Stop when running out of removals (k = 0). 
  Count the number of entries remaining.
"""


def least_unique_nums(arr: list[int], k: int) -> int:
    frequency_dict: dict[int, int] = {}
    for num in arr:
        if num not in frequency_dict:
            frequency_dict[num] = 0
        frequency_dict[num] += 1

    sorted_frequencies = sorted(frequency_dict.values(), reverse=True)

    while k > 0:
        min_frequency = sorted_frequencies[-1]
        if min_frequency > k:
            break
        k -= min_frequency
        sorted_frequencies.pop()

    return len(sorted_frequencies)


"""
Complexity:
- Let n = len(arr)
  constraint: 0 <= k <= n

1. Time complexity:
- Build frequency_dict: O(n)
- Sort the frequencies: O(n*log(n)) (worst case when all elements are unique)
- Remove k elements: O(k) (worst case when all elements are unique)
=> Overall: O(n*log(n) + n + k) = O(n*log(n))

2. Space complexity: O(n)
(worst case when all elements are unique)
- hash map: O(n)
- frequencies array: O(n)
- sort frequencies: O(n) (timsort) 
"""


# === Another approach: use min heap ===
"""
- After collecting frequencies of unique numbers,
  add all frequencies to a min heap.
- At any step, pick the smallest frequency f (heappop).
- If f <= k, decrease k by f.
  Otherwise, return len(heap) + 1 (+1 for the just-popped item)
- When k = 0, return len(heap).
"""

import heapq


def least_unique_nums(arr: list[int], k: int) -> int:
    frequency_dict: dict[int, int] = {}
    for num in arr:
        if num not in frequency_dict:
            frequency_dict[num] = 0
        frequency_dict[num] += 1

    frequencies = list(frequency_dict.values())
    heapq.heapify(frequencies)  # convert to min heap

    while k > 0:
        min_frequency = heapq.heappop(frequencies)
        if min_frequency > k:
            return len(frequencies) + 1
        k -= min_frequency

    return len(frequencies)


"""
Complexity:
(worst case when all elements are unique)

1. Time complexity: 
- Build frequency_dict: O(n)
- Generate 'frequencies' list: O(n) 
- Heapify 'frequencies': O(n)
- Remove k elements: O(k * log(n)) (heappop takes O(log(n)))
=> Overall: O(n + k*log(n)) = O(n*log(n))

2. Space complexity: O(n)
(worst case when all elements are unique)
- frequency_dict: O(n)
- 'frequencies' heap: O(n)
"""