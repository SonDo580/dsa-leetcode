"""
Key idea:
- Repeatedly sort the elements by digits,
  from the least significant to the most significant.
  Then the final sorted order is achieved.
- If 2 elements have the same ith digit,
  the one with smaller (i-1)th digit should come first.
  -> Each pass should use a stable sorting algorithm to
     preserve earlier ordering.
  -> Counting sort is efficient,
     since the number of digits is small and fixed (10 digits).
"""

import math


def radix_sort(arr: list[int]) -> None:
    if not arr:
        return

    # Find the maximum number of digits in a number
    max_digits = count_digits(max(arr))

    # Sort by each digit (least significant -> most significant)
    for k in range(max_digits):
        counting_sort_by_digit(arr, k)


def counting_sort_by_digit(arr: list[int], k: int) -> None:
    # Count frequency of each digit
    count = [0] * 10
    for num in arr:
        d = get_kth_digit(num, k)
        count[d] += 1

    # Compute prefix sum (cumulative count)
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build sorted array (iterate in reverse order to keep it stable)
    n = len(arr)
    sorted_arr = [0] * n
    for num in reversed(arr):
        d = get_kth_digit(num, k)
        sorted_arr[count[d] - 1] = num
        count[d] -= 1

    # Copy sorted array back to original array
    for i in range(n):
        arr[i] = sorted_arr[i]


def count_digits(num: int) -> int:
    if num == 0:
        return 1
    return int(math.log10(num)) + 1


def get_kth_digit(num: int, k: int) -> int:
    return num // (10**k) % 10


"""
Complexity:
- Let n = len(arr)
      d = maximum number of digits in a number 
      b = base of the number system (10 in this case)
      
1. Time complexity:
- counting sort: O(n + b)
- sort by each digit: d times 
=> Overall: O(d * (n + b))

2. Space complexity: O(n + b) for counting sort
"""

"""
Feature:
- non-comparison-based sorting algorithm.
- efficient for: 
  + integers.
  + fixed-size strings with small number of characters.
"""
