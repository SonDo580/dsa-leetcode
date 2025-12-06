"""
https://leetcode.com/problems/kth-largest-element-in-an-array

Given an integer array nums and an integer k,
return the kth largest element in the array.

Note that it is the kth largest element in the sorted order,
not the kth distinct element.

Can you solve it without sorting?
"""

# ========== Approach 1: Min/Max Heap ==========
# ==========================================
# (see Heap section)


# ========== Approach 2: Quick Select ==========
# ==============================================
"""
Idea:
- Randomly choose a pivot.
- Partition 'nums':
  . x < pivot -> put in 'left'.
  . x == pivot -> put in 'mid'.
  . x > pivot -> put in 'right'.
- Check 3 cases:
  . k <= len(right)
    -> the kth largest element is in 'right'.
    -> recurse on 'right' with the same k.
  . k <= len(right) + len(mid)
    -> the kth largest element is in 'mid'.
    -> return pivot value.
  . otherwise:
    -> the kth largest element is in 'left'.
    -> recurse on 'left' with k = k - (len(mid) + len(right))
"""

import random


def find_kth_largest(nums: list[int], k: int) -> int:
    return quick_select(nums, k)


def quick_select(nums: list[int], k: int) -> int:
    pivot = random.choice(nums)
    left, mid, right = [], [], []

    for num in nums:
        if num == pivot:
            mid.append(num)
        elif num < pivot:
            left.append(num)
        else:
            right.append(num)

    if k <= len(right):
        return quick_select(right, k)

    if k <= len(right) + len(mid):
        return pivot

    return quick_select(left, k - len(mid) - len(right))


"""
Complexity:

1. Time complexity:
- We process only 1 partition at each recursion depth (unlike quick sort).
  + Average case: (balanced partition)
    . T = n + n / 2 + n / 4 + ...
  + Worst case: pivot is always the smallest/largest element
    . T = n + (n - 1) + (n - 2) + ...
=> Overall:
   . Average case: O(n)
   . Worst case: O(n^2)

2. Space complexity: 
- left + mid + right: O(n).
- recursion stack:
  . Worst case: O(n) (pivot is always the smallest/largest element).
  . Average case: O(log(n)) (balanced partition).
=> Overall: O(n)
"""


# ========== Quick Select - space optimized ==========
# ====================================================
"""
- Rearrange 'nums' in-place instead of creating 3 extra arrays.
- Iteratively reduce the search space without recursion. 
"""


def find_kth_largest(nums: list[int], k: int) -> int:
    return quick_select(nums, k, start=0, end=len(nums) - 1)


def quick_select(nums: list[int], k: int, start: int, end: int) -> int:
    while start <= end:
        pivot = nums[random.randint(start, end)]

        # Push x < pivot to the left
        mid_start = start
        for i in range(start, end + 1):
            if nums[i] < pivot:
                nums[mid_start], nums[i] = nums[i], nums[mid_start]
                mid_start += 1

        # Push x > pivot to the right
        mid_end = end
        for i in range(end, mid_start - 1, -1):
            if nums[i] > pivot:
                nums[mid_end], nums[i] = nums[i], nums[mid_end]
                mid_end -= 1

        # Search the (x > pivot) partition
        if k <= end - mid_end:
            start = mid_end + 1

        # Result is in (x == pivot) partition
        elif k <= end - mid_start + 1:
            return pivot

        # Search the (x < pivot) partition
        else:
            k -= end - mid_start + 1
            end = mid_start - 1


"""
Complexity:

1. Time complexity:
- Average case: O(n)
- Worst case: O(n^2)

2. Space complexity: O(1)
"""
