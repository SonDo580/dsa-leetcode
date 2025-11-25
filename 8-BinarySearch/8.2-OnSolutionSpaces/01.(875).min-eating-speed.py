"""
https://leetcode.com/problems/koko-eating-bananas

Koko loves to eat bananas.
There are n piles of bananas, the ith pile has piles[i] bananas.
The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k.
Each hour, she chooses some pile of bananas and eats k bananas from that pile.
If the pile has less than k bananas,
she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.

Example 1:
Input: piles = [3,6,7,11], h = 8
Output: 4

Example 2:
Input: piles = [30,11,23,4,20], h = 5
Output: 30

Example 3:
Input: piles = [30,11,23,4,20], h = 6
Output: 23

Constraints:
1 <= piles.length <= 10^4
piles.length <= h <= 10^9
1 <= piles[i] <= 10^9
"""

"""
Analysis:
- If Koko can eat all bananas with eating speed k, then:
  + she can eat all bananas with any k' > k
  + she can not eat all bananas with any k' < k
  -> We can binary search for the answer

- Solution space:
  + k must be a positive integer (0 means Koko doesn't eat at all)
    => lower bound: k = 1
  + Eating each pile will takes at least 1 hour.
    Koko eats all the pile if piles[i] <= k, and won't eat the next pile during the hour.
    -> upper bound: k = max(piles)

- To check if an eating speed k is valid:
  + the number of hours required to eat a pile is bananas / k, rounded up.
  -> Iterate over the input, sum the values of ceil(bananas / k),
     and check if the hours is within the limit h.
- If k is valid try to find smaller k. Otherwise try a bigger k.

- Constraint note: piles.length <= h
  . without this condition, there's no valid k if piles.length > h,
    since each eating pipe takes at least 1 hour
"""


import math


def min_eating_speed(piles: list[int], h: int) -> int:
    def _is_valid(k: int) -> bool:
        """Check if can eat all piles in h hours with eating speed k."""
        hours = 0
        for bananas in piles:
            hours += math.ceil(bananas / k)
        return hours <= h

    left = 1
    right = max(piles)

    while left <= right:
        mid = (left + right) // 2
        if _is_valid(mid):
            right = mid - 1  # search the left portion for smaller k
        else:
            left = mid + 1  # search the right portion for valid k

    return left


"""
Complexity:
Let n = piles.length; k = max(piles)

1. Time complexity:
- check valid k: O(n)
- binary search for min k: O(log(k))
=> Overall: O(n * log(k))

2. Space complexity: O(1)
"""
