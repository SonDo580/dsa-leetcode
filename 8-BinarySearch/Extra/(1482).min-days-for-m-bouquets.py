"""
https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets

You are given an integer array 'bloomDay', an integer m and an integer k.
You want to make m bouquets.
To make a bouquet, you need to use k adjacent flowers from the garden.
The garden consists of n flowers,
the ith flower will bloom in the bloomDay[i] and then can be used in exactly one bouquet.
Return the minimum number of days you need to wait to be able to make m bouquets from the garden.
If it is impossible to make m bouquets return -1.
"""

"""
Analysis:
- It's impossible to make m bouquets if floor(num_flowers / k) < m
- The longer we wait, the more flowers to use.
  -> . Use binary search to find the min valid answer.
     . Solution space: min bloom day -> max bloom day.
- Flowers grouping:
  + A flower should always be grouped with previous ones
    if the current bouquet hasn't been full.
  + If we group it with later flowers, the total number of bouquets
    will be less than or at most equal.
"""


def min_days(bloom_day: list[int], m: int, k: int) -> int:
    def max_bouquets(wait_days: int) -> int:
        """
        Return the maximum number of bouquets that can be made
        after waiting for 'wait_days' days.
        """
        num_bouquets: int = 0
        num_consecutive_bloomed_flowers: int = 0

        for day in bloom_day:
            if day <= wait_days:
                num_consecutive_bloomed_flowers += 1
            else:
                num_bouquets += num_consecutive_bloomed_flowers // k
                num_consecutive_bloomed_flowers = 0

        num_bouquets += num_consecutive_bloomed_flowers // k
        return num_bouquets

    # Not enough flowers to make m bouquets
    if len(bloom_day) // k < m:
        return -1

    left = min(bloom_day)
    right = max(bloom_day)
    min_wait_days = -1

    while left <= right:
        mid = (left + right) // 2
        if max_bouquets(mid) >= m:
            min_wait_days = mid  # update best result so far
            right = mid - 1  # search left for better result
        else:
            left = mid + 1  # search right for valid result

    return min_wait_days


"""
Complexity:
- Let n = bloom_day.length
      k = max(bloom_day)

1. Time complexity:
- Find boundaries (left, right): O(n)
- Binary search: 
  + O(log(k)) iterations
  + Count bouquets in each iteration: O(n)
=> Overall: O(n * log(k))

2. Space complexity: O(1)
"""
