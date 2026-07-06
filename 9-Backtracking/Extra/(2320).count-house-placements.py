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
"""


# === 1) Exceed time limit ===
def count_house_placements(n: int) -> int:
    num_placements_one_side = 0

    def place(i: int, last_used: bool) -> int:
        """Place or don't place house at ith slot on 1 side."""
        nonlocal num_placements_one_side

        # Base case: all slots have been considered
        if i == n:
            num_placements_one_side += 1
            return

        # Option 1: Don't place a house at current slot
        place(i + 1, last_used=False)

        # Option 2: Place a house at current slot if last slot is empty
        if not last_used:
            place(i + 1, last_used=True)

    place(i=0, last_used=False)
    num_placements_both_sides = num_placements_one_side**2
    return num_placements_both_sides % 1_000_000_007


"""Complexity:

1. Time complexity: O(2^n)
- branching factor: O(2)
  (Each 'place' call spans at most 2 more 'place' calls)
- recursion depth: O(n)
=> Total work: branching_factor^recursion_depth = O(2^n)
 
2. Space complexity: O(n) for recursion stack
"""


# === 2) Optimize (becomes Top-down DP) ===
"""
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
- Number of DP states: O(n*2)
=> Total work: O(n*2) * O(1) = O(n)

2. Space complexity: O(n)
- recursion stack: O(n)
- memoization: O(n*2) = O(n)
"""


# === 3) Bottom-up DP ===
def count_house_placements(n: int) -> int:
    # dp[last_used][i]: number of valid placements (on 1 side) for given states
    dp = [[0] * (n + 1) for _ in range(2)]

    # Base case: all slots have been considered
    dp[0][n] = dp[1][n] = 1

    # dp[last_used][i] depends on both dp[False][i+1] and dp[True][i+1]
    # -> must calculate all last_used entries for (i+1)th slot
    #    before moving to ith slot
    # -> loop order is important
    for i in range(n - 1, -1, -1):
        for last_used in range(2):
            # Don't place a house at (i+1)th slot
            # -> ith slot is empty or occupied
            dp[last_used][i] += dp[0][i + 1]

            # Place a house at (i+1)th slot
            # -> ith slot must be empty
            if not last_used:
                dp[last_used][i] += dp[1][i + 1]

    num_placements_one_side = dp[0][0]
    num_placements_both_sides = num_placements_one_side**2
    return num_placements_both_sides % 1_000_000_007


"""Complexity:
1. Time complexity: O(n*2) = O(n)
2. Space complexity: O(n*2) = O(n) for 'dp' matrix
"""

# === 4) Bottom-up DP (optimize space) ===
"""
- dp[...][i] only depends on dp[...][i+1] 
  -> use 2 variables to track dp[0][i+1] and dp[1][i+1]
"""


def count_house_placements(n: int) -> int:
    # Base case: all slots have been considered
    false_next_i = true_next_i = 1  # dp[0][n] = dp[1][n] = 1

    for _ in range(n - 1, -1, -1):
        # Don't place a house at (i+1)th slot
        # -> ith slot is empty or occupied
        false_i = true_i = false_next_i  # dp[last_used][i] += dp[0][i + 1]

        # Place a house at (i+1)th slot
        # -> ith slot must be empty
        false_i += true_next_i  # dp[0][i] += dp[1][i + 1]

        false_next_i, true_next_i = false_i, true_i

    num_placements_one_side = false_next_i  # dp[0][0]
    num_placements_both_sides = num_placements_one_side**2
    return num_placements_both_sides % 1_000_000_007


"""Complexity:
1. Time complexity: O(n*2) = O(n)
2. Space complexity: O(1)
"""
