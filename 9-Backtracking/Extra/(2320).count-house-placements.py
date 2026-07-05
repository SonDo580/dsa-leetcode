"""
https://leetcode.com/problems/count-number-of-ways-to-place-houses/

There is a street with n * 2 plots,
where there are n plots on each side of the street.
The plots on each side are numbered from 1 to n.
On each plot, a house can be placed.

Return the number of ways houses can be placed such that
no two houses are adjacent to each other on the same side of the street.
Since the answer may be very large, return it modulo 10^9 + 7.

Note that if a house is placed on the ith plot on one side of the street,
a house can also be placed on the ith plot on the other side of the street.
"""

"""
Idea:
- Placements on both sides of the street is independent and symmetric.
  -> Find different placements on 1 side then calculate the total 
     . num_placements_both_sides = num_placements_one_side^2
       (group each placement on 1 side with all placements on the other side)

Backtracking to find all valid placements for 1 side:
- States needed:
  . i: current slot to check.
  . last_used: True if last slot is occupied.
- A house can be placed at i if last_used = False (no adjacent houses).
- Base case: all slots have been considered.

Optimize (becomes Top-down DP):
- There are overlapping sub-problems -> should cache results
- Example:
  . [1, 0, 0, i]
  . [1, 1, 0, i]
  -> reach the same (i, last_used) from different paths.
"""

from functools import cache


def count_house_placements(n: int) -> int:
    @cache
    def count(i: int, last_used: bool) -> int:
        """Return number of valid placements for the given states."""
        # Base case: all slots have been considered
        if i == n:
            return 1

        cnt = 0

        # Option 1: Don't place a house at current slot
        cnt += count(i + 1, last_used=False)

        # Option 2: Place a house at current slot if last slot is empty
        if not last_used:
            cnt += count(i + 1, last_used=True)

        return cnt

    num_placements_one_side = count(i=0, last_used=False)
    num_placements_both_sides = num_placements_one_side**2
    return num_placements_both_sides % 1_000_000_007


"""Complexity:

1. Time complexity: O(n)
- Number of DP states: O(n*2) = O(n)
=> Total work: O(n) * O(1) = O(n)

2. Space complexity: O(n)
- recursion stack: O(n)
- memoization: O(n*2) = O(n)
"""
