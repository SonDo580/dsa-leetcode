"""
https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/

Given the array 'nums', 
for each nums[i] find out how many numbers in the array are smaller than it. 
That is, for each nums[i] you have to count the number of valid j's 
such that j != i and nums[j] < nums[i].

Return the answer in an array.
"""

"""
Idea:
- Sort 'nums' in ascending order.
- For nums[i], there are 2 cases:
  . nums[i] == nums[i - 1]:
    -> number of smaller elements doesn't change.
  . nums[i] > nums[i - 1]
    -> all items in nums[0..i-1] is smaller than nums[i] (count = i).
- Base case: nums[0] has no smaller elements.
- To map answers to correct positions,
  the sorted array should also store original indices, not just values.
"""


def smaller_numbers_than_current(nums: list[int]) -> list[int]:
    n = len(nums)

    # Collect values with indices
    val_idx_pairs: list[tuple, int] = []
    for i, num in enumerate(nums):
        val_idx_pairs.append((num, i))

    # Sort in ascending order by values
    val_idx_pairs.sort()

    ans: list[int] = [0] * n
    for i in range(1, n):
        curr_val, curr_idx = val_idx_pairs[i]
        prev_val, prev_idx = val_idx_pairs[i - 1]

        if curr_val == prev_val:
            ans[curr_idx] = ans[prev_idx]
        else:
            # curr_val > prev_val
            ans[curr_idx] = i

    return ans


"""
Complexity:

1. Time complexity: O(n * log(n))
- Collect values with indices: O(n)
- Sort value-index pairs: O(n * log(n))
- Build answer array: O(n)

2. Space Complexity: O(n)
- 'val_idx_pairs': O(n)
- sort 'val_idx_pairs': O(n) (Python's timsort)
"""
