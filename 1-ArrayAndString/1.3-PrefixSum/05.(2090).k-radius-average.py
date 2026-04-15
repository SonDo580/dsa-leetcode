"""
https://leetcode.com/problems/k-radius-subarray-averages/

You are given a 0-indexed array 'nums' of n integers, and an integer k.

The k-radius average for a subarray of 'nums' centered at some index i
with the radius k is the average of all elements in nums between
the indices i - k and i + k (inclusive).
If there are less than k elements before or after the index i,
then the k-radius average is -1.

Build and return an array 'avgs' of length n where avgs[i] is
the k-radius average for the subarray centered at index i.

The average of x elements is the sum of the x elements divided by x,
using integer division. The integer division truncates toward zero,
which means losing its fractional part.
"""

"""
Special cases:
. k = 0 
  -> n 1-element sub-arrays 
  -> avgs = nums
. k > n // 2 
  -> all sub-arrays don't have enough k elements on both sides
  -> avgs = [-1] * n

Normal case:
- We need a way to quickly find sum([i-k..i+k])
  -> Use prefix sum
- Formula:
  . sum([x..y]) = prefix[y] - prefix[x-1]
                = prefix[y] - prefix[x] + nums[x] 
  . use the second formula to avoid dealing with x=0
"""


def get_k_radius_averages(nums: list[int], k: int) -> list[int]:
    if k == 0:
        return nums

    n = len(nums)
    if k > (n // 2):
        return [-1] * n

    prefix_sum = [nums[0]]
    for i in range(1, n):
        prefix_sum.append(prefix_sum[-1] + nums[i])

    avgs: list[int] = []
    count = 2 * k + 1  # number of elements in (full) k-radius sub-array

    for i in range(n):
        left = i - k
        right = i + k
        if left < 0 or right > n - 1:
            avgs.append(-1)
        else:
            arr_sum = prefix_sum[right] - prefix_sum[left] + nums[left]
            avgs.append(arr_sum // count)

    return avgs


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(n) for prefix_sum
"""
