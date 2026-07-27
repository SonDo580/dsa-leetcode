"""
https://leetcode.com/problems/increasing-triplet-subsequence/

Given an integer array nums,
return true if there exists a triple of indices (i, j, k)
such that i < j < k and nums[i] < nums[j] < nums[k].
If no such indices exists, return false.
"""

# === Approach 1: Brute-force (exceed time limit) ===
"""
- For each nums[i], check all nums[j] after it.
  For each of those nums[j], check all nums[k] after it.
"""


class Solution:
    def increasingTriplet(self, nums: list[int]) -> bool:
        n = len(nums)
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    if nums[i] < nums[j] < nums[k]:
                        return True
        return False


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n^3)
2. Space complexity: O(1)


=== Time complexity in detail (v1) ===
- i loop: runs from 0 to n - 3
  j loop: runs from i + 1 to n - 2
  k loop: runs from j + 1 to n - 1 
- Total number of innermost loop iterations:
  S = sum(
        sum(
            sum(1 for k in [j+1..n-1])
            for j in [i+1..n-2]
        )
        for i in [0..n-3]
      )

. sum(1 for k in [j+1..n-1]) = n-1-j

. sum(n-1-j for j in [i+1..n-2])
  . Let m = n-1-j
  -> m in [n-1-(i+1)..n-1-(n-2)] = [n-i-2..1]
  -> sum(n-1-j for j in [i+1..n-2]) 
     = sum(m for m in [1..n-i-2]) 
     = (n-i-2)*(n-i-1)/2

. S = sum((n-i-2)*(n-i-1)/2 for i in [0..n-3])
  . Let p = n-i-2
  -> p in [n-0-2..n-(n-3)-2] = [n-2..1]
  -> S = sum(p*(p + 1)/2 for p in [1..n-2])
     = 1/2 * (sum(p^2 for p in [1..n-2]) + sum(p for p in [1..n-2]))
  . sum(x for x in [1..X]) = X*(X+1) / 2
  . sum(x^2 for x in [1..X]) = X*(X+1)*(2*X+1) / 6
  -> S = 1/2 * ((n-2)*(n-1) / 2 + (n-2)*(n-1)*(2*n-3) / 6))
       = ((n-2)*(n-1) / 4) * (1 + (2*n-3) / 3)
       = ((n-2)*(n-1) / 4) * (2*n / 3)
       = (n-2)*(n-1)*n / 6
       = O(n^3)


=== Time complexity in detail (v2) ===
- Number of valid triplets (i, j, k) such that 0 <= i < j < k <= n-1
  <-> Number of ways to choose 3 distinct indices from n elements.
  -> S = nC3 = n! / (3! * (n-3)!)
       = (n-2)*(n-1)*n / 6
"""


# === Approach 2: DP (exceed time limit) ===
"""
Identify DP problem:
- Local decision affect future decision:
  . use nums[i] -> can only choose nums[j] > nums[i] later
- Overlapping sub-problems:
  . ex: multiple triplets (i, j, k) can share the same (i, j)

Implementation:
- Let dp[i] be length of the longest strictly increasing subsequence that ends at i.
- Base case: each nums[i] is a 1-item subsequence.   
- Recurrence: dp[i] = max(dp[i], 1 + dp[j] for j in [0..i-1] if nums[j] < nums[i])
- While building dp, if dp[i] can reach 3, return True.
"""


class Solution:
    def increasingTriplet(self, nums: list[int]) -> bool:
        n = len(nums)
        dp = [1] * n  # each nums[i] forms a 1-item subsequence
        for i in range(1, n):
            for j in range(i):
                if nums[j] >= nums[i]:
                    continue
                dp[i] = max(dp[i], 1 + dp[j])
                if dp[i] == 3:
                    return True
        return False


"""
Complexity:

1. Time complexity: O(n^2)
- Init 'dp': O(n)
- Loop: sum(i for i in [1..n-1]) = 1 + 2 + ... + n-1 = n*(n-1)/2 = O(n^2) 

2. Space complexity: O(n) for 'dp'
"""


# === Approach 3: Binary search ===
"""
- nums[i] can extend a previous subsequence if nums[i] > subsequence tail
  -> Check the subsequence with smallest tail.
- Let tails[L] be the smallest tail of the LIS with length L+1
- Case 1: nums[i] > tails[-1], appends it to tail.
  Case 2: nums[i] < tails[-1] 
          -> nums[i] can serve as a smaller tail for a previous length
          -> Find smallest L such that tails[L] >= nums[i].
             Update tails[L] = nums[i]
             (Later numbers can extend from it instead of previous tails[L])
  -> Consequence: 'tails' is strictly increasing
  -> Can use binary search in case 2
- If len(tails) reaches 3 at any point, return True.
"""

from bisect import bisect_left


class Solution:
    def increasingTriplet(self, nums: list[int]) -> bool:
        tails: list[int] = []
        for num in nums:
            if len(tails) == 0 or num > tails[-1]:
                tails.append(num)
                if len(tails) == 3:
                    return True
            elif num < tails[-1]:
                idx = bisect_left(tails, num)
                tails[idx] = num
        return False


"""
Complexity:
- Stop when len(tails) == 3

1. Time complexity: O(n*log(2)) = O(n)
2. Space complexity: O(3) = O(1) for 'tails'
"""


# === Approach 3.1: Linear search ===
"""
- Don't need binary search since the size is small
  (stop when len(tails) == 3 -> only search at most 2 items)
"""


class Solution:
    def increasingTriplet(self, nums: list[int]) -> bool:
        tails: list[int] = []
        for num in nums:
            if len(tails) == 0 or num > tails[-1]:
                tails.append(num)
                if len(tails) == 3:
                    return True
            elif num < tails[-1]:
                for i in range(len(tails)):
                    if tails[i] >= num:
                        tails[i] = num
                        break
        return False


"""
Complexity:
- Stop when len(tails) == 3

1. Time complexity: O(n*2) = O(n)
2. Space complexity: O(3) = O(1) for 'tails'
"""


# === Approach 3.2: Reduce space ===
"""
- Don't need 'tails' array. Use 2 variables 
  . first <-> tails[0]
  . second <-> tails[1].
- When encounter num > second, return True.

Notes:
- 'first' doesn't need to come before 'second' in original 'nums'.
  They are just smallest tail (so far) for a subsequence of length 1 and 2.
"""


class Solution:
    def increasingTriplet(self, nums: list[int]) -> bool:
        first = second = None

        for num in nums:
            if first is None or num < first:
                first = num
            elif num > first:
                if second is None or num < second:
                    second = num
                elif num > second:
                    return True

        return False


"""
Complexity:
1. Time complexity: O(n) = O(n)
2. Space complexity: O(1)
"""
