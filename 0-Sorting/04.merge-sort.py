# ===== Key idea =====
# (divide and conquer)
# - Divide the array into 2 halves.
# - Recursively sort each half.
# - Merge the 2 sorted arrays into a single sorted array.


def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[:mid])

    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    """Merge 2 sorted lists into 1 sorted list."""
    result: list[int] = []
    i = j = 0

    # Compare elements from both lists and pick the smaller one.
    # If there's a tie, pick the element from 'left' to ensure stability.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append remaining elements from 'left' or 'right'
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ===== Complexity =====
# 1. Time complexity: O(n * log(n))
# - The array is split into log_2(n) levels (halving each time).
# - At each level, merging takes O(n).
# -> Total: O(n * log(n))
#
# 2. Space complexity: O(n)
# - Space for 'result' array created during merge.
#   In the last merge, 'result' has n elements.

# ===== Stability =====
# - Stable:
#   + Because when merging, we pick the element from 'left' if there's a tie

# ===== Extra details =====
# Why the array is split into log_2(n) levels?
# - Suppose we start with an array of size n
#   + level 0: size = n (full array)
#   + level 1: size = n / 2 (each half)
#   + ...
#   + level k: size = n / 2^k (per sub-array)
# - Keep splitting until each sub-array has size 1
#   . n / 2^k = 1 -> k = log_2(n)


# ===== Iterative approach =====
# - Instead of recursively splitting, start with sub-array of size 1.
# - Iteratively merge pairs of sub-arrays, doubling the size each round.
# - Still use the 'merge' function to merge 2 sorted arrays.


def merge_sort_iter(arr: list[int]) -> list[int]:
    n = len(arr)
    size = 1  # current sub-array size to merge

    while size < n:
        # Merge sub-arrays in pairs
        for i in range(0, n, 2 * size):
            left = arr[i : i + size]
            right = arr[i + size : i + 2 * size]
            arr[i : i + 2 * size] = merge(left, right)

        # Double the sub-array size each round
        size *= 2

    return arr
