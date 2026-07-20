"""
https://leetcode.com/problems/count-of-smaller-numbers-after-self/

Given an integer array 'nums',
return an integer array 'counts' where counts[i] is
the number of smaller elements to the right of nums[i].
"""

# === Approach 1: Brute-force (exceed time limit) ===
"""
- For each nums[i], iterate through nums[i+1:] to find smaller elements.
"""


def count_smaller(nums: list[int]) -> list[int]:
    n = len(nums)
    count: list[int] = [0] * n
    for i in range(n - 1):
        for j in range(i + 1, n):
            if nums[j] < nums[i]:
                count[i] += 1
    return count


"""
Complexity:
1. Time complexity: O(n^2)
2. Space complexity: O(1)
"""


# === Approach 2: Merge Sort ===
"""
- When merging 2 arrays 'left' and 'right'.
  . All items in 'right' are to the right of all items in 'left'.
  . If left[i] > right[j]:
    . If sort in ascending order:
      -> all items in left[i:] > right[j]
      -> increment count for all items in left[i:]
         (inefficient)
    . If sort in descending order:
      -> left[i] > all items in right[j:]
      -> count for left[i] increases by len(right)-j
  -> Sort in descending order.
- We need to track original index i to update count[i] 
  -> group index and value before sorting.
"""


def count_smaller(nums: list[int]) -> list[int]:
    n = len(nums)
    count: list[int] = [0] * n
    nums_with_indices = [(num, i) for i, num in enumerate(nums)]
    _merge_sort(nums_with_indices, 0, n - 1, count)
    return count


def _merge_sort(
    nums_with_indices: list[tuple[int, int]], left: int, right: int, count: list[int]
) -> None:
    """
    Sort nums_with_indices in descending order.
    Record number of smaller items to the right of each item.
    """
    if left == right:
        return

    mid = (left + right) // 2
    _merge_sort(nums_with_indices, left, mid, count)
    _merge_sort(nums_with_indices, mid + 1, right, count)
    _merge(nums_with_indices, left, mid, right, count)


def _merge(
    nums_with_indices: list[tuple[int, int]],
    left: int,
    mid: int,
    right: int,
    count: list[int],
) -> None:
    """
    Merge 2 arrays sorted in descending order.
    Record number of smaller items to the right of each item.
    """
    sorted_arr: list[tuple[int, int]] = []
    i = left
    j = mid + 1

    while i <= mid and j <= right:
        left_val, left_idx = nums_with_indices[i]
        right_val, _ = nums_with_indices[j]
        if left_val > right_val:
            count[left_idx] += right - j + 1
            sorted_arr.append(nums_with_indices[i])
            i += 1
        else:  # unstable sort is acceptable
            sorted_arr.append(nums_with_indices[j])
            j += 1

    while i <= mid:
        sorted_arr.append(nums_with_indices[i])
        i += 1
    while j <= right:
        sorted_arr.append(nums_with_indices[j])
        j += 1

    nums_with_indices[left : right + 1] = sorted_arr


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n*log(n))
- Init count: O(n)
- Group values with indices: O(n)
- Merge sort: O(n*log(n))
  . Sub-array size at each level:
    . n, n / 2, n / 4, ..., n / 2^k
    . n / 2^k = 1 (base case) -> k = log2(n)
    -> Number of levels (recursion depth): O(log(n))
  . Total merge work at each level: O(n)
  -> Work across levels: O(n*log(n))

2. Space complexity: O(n)
- 'num_with_indices': O(n)
- Merge sort: O(n)
  . recursion stack: O(log(n))
  . temporary array for merging: O(n)
"""


# === Approach 3: Segment Tree ===
# TODO
