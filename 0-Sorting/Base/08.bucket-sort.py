"""
Key idea:
- Distribute input elements into multiple buckets.
- Sort every bucket individually (usually use insertion sort).
- Concatenate all buckets to get the final sorted array.
"""


def bucket_sort(arr: list[float]) -> None:
    """Sort floating-point numbers in range [0, 1]."""
    n = len(arr)
    buckets = [[] for _ in range(n)]

    # Place elements into buckets
    for num in arr:
        bucket_idx = int(n * num)
        buckets[bucket_idx].append(num)

    # Sort individual buckets
    for bucket in buckets:
        insertion_sort(bucket)

    # Concatenate buckets to original array
    k = 0
    for bucket in buckets:
        for num in bucket:
            arr[k] = num
            k += 1


def insertion_sort(bucket: list[float]) -> None:
    n = len(bucket)

    for i in range(1, n):
        current = bucket[i]  # current element to insert
        j = i - 1  # end of sorted portion

        # Shift element of the sorted portion to the right
        # until we find the correct position for current
        while j >= 0 and bucket[j] > current:
            bucket[j + 1] = bucket[j]
            j -= 1

        # Insert current at the correct position in the sorted portion
        bucket[j + 1] = current


"""
Complexity:
- Let n = len(arr)
      k = number of buckets

1. Time complexity:
- Put elements into buckets: O(n)
- Sorting k buckets:
  + Worst case: 1 bucket gets all the elements
    -> insertion sort that 1 bucket: O(n^2)
  + Best case: uniform distribution
    -> insertion sort each bucket: O(1)
- Copy elements from buckets back: O(n)
=> Overall:
   . Worst case: O(n^2)
   . Best case: O(n + k)

2. Space complexity:
- 'buckets': O(k)
- items in all 'buckets': O(n)
=> Overall: O(n + k)
"""

"""
Stability: stable
- Because we use insertion sort (which is stable) for individual buckets.
"""

"""
Features:
- work well if elements are uniformly distributed across a range.
"""
