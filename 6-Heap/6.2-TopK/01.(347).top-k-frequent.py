"""
https://leetcode.com/problems/top-k-frequent-elements/

Given an integer array 'nums' and an integer k,
return the k most frequent elements.
You may return the answer in any order.

Follow up: Your algorithm's time complexity must be better than O(n log n),
where n is the array's size.
"""

"""
Idea:
- Time complexity must be better than O(n*log(n)) 
  -> cannot use sorting.

Implementation (use heap):
- Iterate over input and add items to a min heap (by frequency).
- When the heap size exceeds k, pop the least frequent item.
- In the end, the k most frequency items remain on the heap.
"""


from collections import Counter
import heapq


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    frequency_dict = Counter(nums)
    heap: list[tuple[int, int]] = []  # min heap

    for num, freq in frequency_dict.items():
        # push the tuple (frequency, num)
        heapq.heappush(heap, (freq, num))

        # pop item with min frequency when heap size exceed k
        if len(heap) > k:
            heapq.heappop(heap)

    return [item[1] for item in heap]


"""
Complexity:

1. Time complexity:
- Create 'frequency_dict': O(n)
- Iterate through 'frequency_dict': at most n iterations
  . heap operations: O(log(k)) (max heap size is k)
=> Overall: O(n*log(k))

2. Space complexity:
- 'frequency_dict': O(n)
- heap: O(k)
=> Overall: O(n + k)
"""

# === Alternative (complexity not satisfy follow-up) ===
"""
- Use a max heap (by frequency).
- Push all elements onto the heap.
- Pop k most frequent elements off the heap.
"""


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    frequency_dict = Counter(nums)
    heap: list[tuple[int, int]] = []  # max heap

    for num, freq in frequency_dict.items():
        heapq.heappush(heap, (-freq, num))

    # pop k most frequent items
    ans: list[int] = []
    for _ in range(k):
        ans.append(heapq.heappop(heap)[1])

    return ans


"""
Complexity:

1. Time complexity:
- Create 'frequency_dict': O(n)
- Iterate through 'frequency_dict': at most n iterations
  . heappush: O(log(n))
- Build 'ans': k iterations
  . heappop: O(log(n))
=> Overall: O(n) + O(n*log(n)) + O(k*log(n)) = O((n+k)*log(n))

2. Space complexity:
- 'frequency_dict': O(n)
- heap: O(n)
=> Overall: O(n)
"""
