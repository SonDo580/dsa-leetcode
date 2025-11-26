"""
https://leetcode.com/problems/frequency-of-the-most-frequent-element

You are given an integer array nums and an integer k.
In one operation, you can choose an index of nums and increment the element at that index by 1.
Return the maximum possible frequency of an element after performing at most k operations.

Example 1:
Input: nums = [1,2,4], k = 5
Output: 3
Explanation: Increment the first element three times and the second element two times to make nums = [4,4,4].
4 has a frequency of 3.

Example 2:
Input: nums = [1,4,8,13], k = 5
Output: 2
Explanation: There are multiple optimal solutions:
- Increment the first element three times to make nums = [4,4,8,13]. 4 has a frequency of 2.
- Increment the second element four times to make nums = [1,8,8,13]. 8 has a frequency of 2.
- Increment the third element five times to make nums = [1,4,13,13]. 13 has a frequency of 2.

Example 3:
Input: nums = [3,9,6], k = 2
Output: 1

Constraints:
1 <= nums.length <= 10^5
1 <= nums[i] <= 10^5
1 <= k <= 10^5
"""

"""
Analysis:
- For each value x, try increasing lower values to x, then find x's final frequency.
- To make better use of k, we should prioritize using greater values.

- Optimization: 
  + Sort 'nums' for faster checking.
  + Instead of trying each value sequentially, 
    use binary search to find the farthest index j,
    such that all elements from j to current index i
    requires at most k operations to transform into nums[i]
  + The final frequency of nums[i] is then the size of the window [j..i]

- Find the number of operations needed to transform 
  all elements from j to i into nums[i]:
  + Formula: nums[i] * (i - j + 1) - sum(nums[j:(i + 1)])
  + Geometric representation: rectangular area - occupied area
            ___
    ___ ___|___|
   |___|___|___|
...|___|___|___|...
     j       i

- To find the sum of a window quickly, build a prefix sum array
  such that prefix_sum[i] = nums[0] + nums[1] + ... + nums[i]
  -> sum(nums[j:(i + 1)]) = prefix_sum[i] - prefix_sum[j - 1]
- To avoid handling edge case (j = 0), let prefix_sum[i] be
  the sum of the window up to but not including i.
  -> . prefix_sum[0] = sum([]) = 0    (empty window)
     . sum(nums[j:(i + 1)]) = prefix_sum[i + 1] - prefix_sum[j]

- Why we only try to increment values to existing ones, 
  instead of creating new values?
  + Let's use the sorted version of 'nums' for easier reasoning. 
  + Suppose we want to convert a window [j..i] into a value T.
    . T < nums[i] -> impossible, since we can only increase values.
    . T > nums[i] -> takes more operations than choosing T = nums[i].
      (cost = T * window_size - window_sum)
    -> choose T = nums[i]
"""


def max_frequency(nums: list[int], k: int) -> int:
    def _count_required_operations(
        nums: list[int], prefix_sum: list[int], left: int, right: int
    ) -> int:
        """
        Count number of operations required to transform all elements
        in nums[left: right + 1] into nums[right]
        """
        window_sum = prefix_sum[right + 1] - prefix_sum[left]
        return nums[right] * (right - left + 1) - window_sum

    def _find_left_bound_within_k_operations(
        nums: list[int], prefix_sum: list[int], i: int
    ) -> int:
        """
        Find the smallest index j such that all elements in nums[j: i + 1]
        can transform to nums[i] within k operations.
        """
        left = 0
        right = i
        j = i

        while left <= right:
            mid = (left + right) // 2
            operations_needed = _count_required_operations(
                nums, prefix_sum, left=mid, right=i
            )
            if operations_needed <= k:
                j = mid  # update best result (smallest j) so far
                right = mid - 1  # search lower half for better result (smaller j)
            else:
                # search upper half for valid result (reduce required operations)
                left = mid + 1

        return j

    nums.sort()
    n = len(nums)

    prefix_sum = [0] * (n + 1)  # prefix_sum[0] is for the empty window
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + nums[i]

    max_freq = 0
    for i in range(n):
        j = _find_left_bound_within_k_operations(nums, prefix_sum, i)
        max_freq = max(max_freq, i - j + 1)

    return max_freq


"""
Complexity:
- Let n = nums.length

1. Time complexity:
- Sort 'nums': O(n * log(n))
- Build prefix_sum: O(n)
- Find left bound within k operations for 1 item: O(log(n))
  -> n items takes O(n * log(n))
=> Overall: O(n * log(n))

2. Space complexity:
- sorting: Python's timsort takes O(n)
- prefix_sum: O(n)
=> Overall: O(n)
"""
