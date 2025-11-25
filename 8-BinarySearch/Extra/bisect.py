# ===== Built-in =====
import bisect

bisect.bisect_left
bisect.bisect_right


# ===== Implementation =====


# Bisect left (lower bound)
def bisect_left(arr: list[int], x: int) -> int:
    """
    Return the index i to insert x in sorted list arr,
    such that all e in a[:i] have e < x and all e in a[i:] have e >= x.

    So if x already exists in arr, i is the leftmost occurrence of x.
    """
    left = 0
    right = len(arr) - 1
    ans = len(arr)

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] >= x:
            ans = mid  # update the best result so far
            right = mid - 1  # search better result on the left side
        else:
            left = mid + 1  # search result on the right side

    return ans


# Bisect right (upper bound)
def bisect_right(nums: list[int], target: int) -> int:
    """
    Return the index i to insert x in sorted list arr,
    such that all e in a[:i] have e <= x and all e in a[i:] have e > x.

    So if x already exists in arr, i is just after the rightmost occurrence of x.
    """
    left = 0
    right = len(nums) - 1
    ans = len(nums)

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] > target:
            ans = mid  # update the best result so far
            right = mid - 1  # search better result on the left side
        else:
            left = mid + 1  # search result on the right side

    return ans
