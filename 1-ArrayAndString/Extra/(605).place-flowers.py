"""
https://leetcode.com/problems/can-place-flowers/

You have a long flowerbed in which some of the plots are planted,
and some are not. However, flowers cannot be planted in adjacent plots.

Given an integer array 'flowerbed' containing 0's and 1's,
where 0 means empty and 1 means not empty, and an integer n,
return true if n new flowers can be planted in the flowerbed
without violating the no-adjacent-flowers rule and false otherwise.
"""

"""
Idea: Greedy
- Plant a flower right when encountering a valid slot.
- If we wait further, the number of flowers that can be planted may reduce.
"""


class Solution:
    def canPlaceFlowers(self, flowerbed: list[int], n: int) -> bool:
        l = len(flowerbed)
        for i in range(l):
            if n == 0:  # no more flowers to plant
                break

            if (
                flowerbed[i] == 1
                or (i > 0 and flowerbed[i - 1] == 1)
                or (i < l - 1 and flowerbed[i + 1] == 1)
            ):  # current slot is not empty or adjacent to a flower
                continue

            # plant 1 flower at current slot (mutate)
            flowerbed[i] = 1
            n -= 1

        return n == 0


"""
Complexity:
- Let L = len(flower_bed)
  -> n <= L

1. Time complexity: O(L)
2. Space complexity: O(1)
"""
