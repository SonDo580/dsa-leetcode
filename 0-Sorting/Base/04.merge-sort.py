"""
Key idea:
(divide and conquer)
- Divide the array into 2 halves.
- Recursively sort each half.
- Merge the 2 sorted arrays into a single sorted array.
"""


def merge_sort(arr: list[int], left: int, right: int) -> None:
    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)


def merge(arr: list[int], left: int, mid: int, right: int) -> None:
    n1 = mid - left + 1
    n2 = right - mid

    # Copy data to temp arrays
    left_arr = [arr[left + i] for i in range(n1)]
    right_arr = [arr[mid + 1 + j] for j in range(n2)]

    # Merge the temp arrays back into arr[left..right]
    # (If there's a tie, pick the element from left_arr to ensure stability)
    i = j = 0
    k = left

    while i < n1 and j < n2:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1

    # Copy remaining items from left_arr/right_arr
    while i < n1:
        arr[k] = left_arr[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = right_arr[j]
        j += 1
        k += 1


"""
Complexity:

1. Time complexity: O(n * log(n))
- The array is split into log_2(n) levels (halving each time).
- At each level, merging takes O(n).
=> Overall: O(n * log(n))

2. Space complexity: O(n)
- Recursion stack: O(log(n))
- Space for temporary arrays used when merging: O(n)
=> Overall: O(n)
"""

"""
Stability: stable
- Because when merging, we pick the element from left_arr if there's a tie
"""

"""
Why the array is split into log_2(n) levels?
- Suppose we start with an array of size n
  + level 0: size = n (full array)
  + level 1: size = n / 2 (each half)
  + ...
  + level k: size = n / 2^k (per sub-array)
- Keep splitting until each sub-array has size 1
  . n / 2^k = 1 -> k = log_2(n)
"""
