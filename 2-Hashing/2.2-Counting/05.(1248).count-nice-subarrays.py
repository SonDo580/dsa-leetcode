"""
https://leetcode.com/problems/count-number-of-nice-subarrays/

Given an array of integers 'nums' and an integer k.
A continuous subarray is called nice if there are k odd numbers in it.
Return the number of nice sub-arrays.
"""

"""
Idea:
- Similar to '(560).subarray-sum-equals-k'.
- Instead of tracking prefix sum, we track number of odd numbers upto an index.

Detailed explanation:
- At each index i, we want to find number of subarray ending at i
  that contains k odd numbers.
- If we have an array of odd_count upto each index,
  we can calculate odd_count in subarray [j..i] quickly:
  . odd_cnt[j..i] = odd_cnt[i] - odd_cnt[j-1] (edge case: j=0).
  (But iterate through the array each time is inefficient)
- To satisfy the condition: 
  . odd_cnt[j-1] = odd_cnt[i] - k
  -> Add odd_count as key to a hashmap for quick lookup.
     Value is number of prefixes with odd_count. 
- Special case for the empty prefix: cnt[0] = 1
  ([] has odd_cnt = 0)
"""

from collections import defaultdict


def nice_subarray_count(nums: list[int], k: int) -> int:
    cnt: defaultdict[int, int] = defaultdict(int)

    cnt[0] = 1
    odd_count: int = 0
    ans: int = 0

    for num in nums:
        odd_count += num % 2
        ans += cnt[odd_count - k]
        cnt[odd_count] += 1

    return ans


"""
Complexity:
1. Time complexity: O(n) - loop through 'nums'
2. Space complexity: O(n) - for 'cnt' dict
"""
