"""
https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

Given a 1-indexed array of integers numbers
that is already sorted in non-decreasing order,
find two numbers such that they add up to a specific target number.
Let these two numbers be numbers[index1] and numbers[index2]
where 1 <= index1 < index2 <= numbers.length.

Return the indices of the two numbers index1 and index2,
each incremented by one, as an integer array [index1, index2] of length 2.

The tests are generated such that there is exactly one solution.
You may not use the same element twice.

Your solution must use only constant extra space.
"""


# ===== Approach 1: Brute-force =====
def two_sum(numbers: list[int], target: int) -> list[int]:
    n = len(numbers)
    for i1 in range(n - 1):
        for i2 in range(i1 + 1, n):
            if numbers[i1] + numbers[i2] == target:
                return [i1 + 1, i2 + 1]
    raise Exception("unreachable")


"""
Complexity:
- Let n = len(numbers)
1. Time complexity: O(n^2)
2. Space complexity: O(1)
"""


# ===== Approach 2: Hash Table =====
def two_sum(numbers: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}  # map seen values to their indices
    for i, num in enumerate(numbers):
        complement = target - num
        if complement in seen:
            return [seen[complement] + 1, i + 1]
        seen[num] = i
    raise Exception("unreachable")


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(n) for 'seen'
"""


# ===== Approach 3: Binary Search =====
"""
- Improve the brute-force version.
- For each i1, instead of searching remaining items sequentially,
  use binary search, since 'numbers' is sorted.
"""


def two_sum(numbers: list[int], target: int) -> list[int]:
    def _binary_search(nums: list[int], left: int, right: int, target: int) -> int:
        """
        Find (any) index with value 'target' in 'nums'.
        Return -1 if not found.
        """
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    n = len(numbers)
    for i1 in range(n - 1):
        i2 = _binary_search(
            nums=numbers, left=i1 + 1, right=n - 1, target=target - numbers[i1]
        )
        if i2 != -1:
            # constraint: there's an exactly 1 solution
            # -> any valid index is the only valid index
            return [i1 + 1, i2 + 1]
    raise Exception("unreachable")


"""
Complexity:
1. Time complexity: O(n * log(n))
2. Space complexity: O(1)
"""


# ===== Approach 4: 2 pointers =====
"""
- Use 2 pointers starting from both ends and move towards each other.
  Let sum = nums[left] + nums[right]
- Since 'nums' is sorted, right-- will decrease 'sum', left++ will increase 'sum'
  -> Adjust 'sum' towards 'target' by moving pointers.
"""


def two_sum(numbers: list[int], target: int) -> list[int]:
    left = 0
    right = len(numbers) - 1
    while left < right:
        sum = numbers[left] + numbers[right]
        if sum == target:
            return [left + 1, right + 1]
        elif sum < target:
            left += 1
        else:
            right -= 1
    raise Exception("unreachable")


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
