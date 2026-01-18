"""
https://leetcode.com/problems/campus-bikes-ii/

On a campus represented as a 2D grid, there are n workers and m bikes, with n <= m.
Each worker and bike is a 2D coordinate on this grid.

We assign one unique bike to each worker so that the sum of the Manhattan distances
between each worker and their assigned bike is minimized.

Return the minimum possible sum of Manhattan distances between each worker and their assigned bike.

The Manhattan distance between two points p1 and p2 is Manhattan(p1, p2) = |p1.x - p2.x| + |p1.y - p2.y|.
"""

# ===== Approach 1.1: Backtracking + set =====
# (exceed time limit)
"""
- Try all possible worker-bike pairs.
- Use a function backtrack(i_worker, used_bikes, total_distance)
  . i_w: current worker
  . used_bikes: a set to track used bikes.
  . total_distance: total Manhattan distance with current assignments.
- Base case: 
  . i_w == n -> all workers have been assigned bikes
    -> update min_distance if total_distance < min_distance 
- At each step, try assigning unused bikes to current worker.
  Accumulate the Manhattan distance and go to the next step.
"""
import math


def assign_bikes(workers: list[tuple[int, int]], bikes: list[tuple[int, int]]) -> int:
    m, n = len(bikes), len(workers)
    min_dist = math.inf

    def manhattan_dist(x: tuple[int, int], y: tuple[int, int]) -> int:
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def backtrack(i_w: int, used_bikes_set: set[int], total_dist: int) -> None:
        nonlocal min_dist
        if i_w == n:
            min_dist = min(min_dist, total_dist)
            return

        for i_b in range(m):
            if i_b not in used_bikes_set:
                used_bikes_set.add(i_b)
                backtrack(
                    i_w + 1,
                    used_bikes_set,
                    total_dist + manhattan_dist(workers[i_w], bikes[i_b]),
                )
                used_bikes_set.remove(i_b)

    backtrack(0, set(), 0)
    return min_dist


"""
Complexity:

1. Time complexity: O(m^n)
- There are m options for the 1st worker.
  For each branch, there are m - 1 options for the 2nd worker.
  ...
  For each branch, there are m - n + 1 options for the nth worker.
-> Number of 'backtrack' calls: m * (m - 1) * ... * (m - n + 1) < m^n
   (This is number of ways to choose n bikes from m bikes
    and arrange them in order: mPn)
   
2. Space complexity: O(n)
- recursion stack: O(n)
- used_bikes_set: O(n) 
  (m >= n, assign to n workers, reused across 'backtrack' calls)
"""


# ===== Approach 1.2: Backtracking + bitmask =====
# (exceed time limit)
"""
- For each bike, we can either use it or not use it
  -> use integer in range 0 to 2^m - 1 to represent used bikes. 
- ith bike is used if ith bit of mask is set:
  . (mask >> i) & 1 = 1
- set ith bit of mask to 1 to mark ith bike as used:
  . new_mask = mask ^ (1 << i)
"""


def assign_bikes(workers: list[tuple[int, int]], bikes: list[tuple[int, int]]) -> int:
    m, n = len(bikes), len(workers)
    min_dist = math.inf

    def manhattan_dist(x: tuple[int, int], y: tuple[int, int]) -> int:
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def backtrack(i_w: int, used_bikes_mask: int, total_dist: int) -> None:
        nonlocal min_dist
        if i_w == n:
            min_dist = min(min_dist, total_dist)
            return

        for i_b in range(m):
            if (used_bikes_mask >> i_b) & 1:
                continue

            new_mask = used_bikes_mask ^ (1 << i_b)
            backtrack(
                i_w + 1,
                new_mask,
                total_dist + manhattan_dist(workers[i_w], bikes[i_b]),
            )

    backtrack(0, 0, 0)
    return min_dist


"""
Complexity:

1. Time complexity: O(m^n)

2. Space complexity: O(n) for recursion stack
"""


# ===== Approach 2.1: Top-down DP =====
"""
- There are overlapping sub-problems. For example:
  . (worker1, bike1), (worker2, bike2)
  . (worker1, bike2), (worker2, bike1)
  . in both cases, when we reach worker3, used_bikes is the same.

- Let dp(i_w, used_bikes_mask) be the minimum total distance between each worker and their assigned bike
  for [i_w..n-1] workers, with used_bikes_mask represents bikes assigned to [0..i_w-1] workers.
- The result is dp(i_w=0, used_bikes_mask=0).
- At each step, try assigning remaining bikes to current worker.
- Base case: i_w = n -> total distance = 0 (no workers)
"""
from functools import cache


def assign_bikes(workers: list[tuple[int, int]], bikes: list[tuple[int, int]]) -> int:
    m, n = len(bikes), len(workers)

    def manhattan_dist(x: tuple[int, int], y: tuple[int, int]) -> int:
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    @cache
    def dp(i_w: int, used_bikes_mask: int) -> int:
        if i_w == n:
            return 0

        min_dist = math.inf
        for i_b in range(m):
            if (used_bikes_mask >> i_b) & 1:
                continue
            dist = manhattan_dist(workers[i_w], bikes[i_b])
            new_mask = used_bikes_mask ^ (1 << i_b)
            min_dist = min(min_dist, dist + dp(i_w + 1, new_mask))
        return min_dist

    return dp(0, 0)


"""
Complexity:

1. Time complexity: O(n * m * 2^m)
- Number of DP states: n * 2^m
- Each state has a loop with m iterations.

2. Space complexity: O(n * 2^m)
- memoization table: O(n * 2^m)
- recursion stack: O(n)
"""


# ===== Approach 2.2: Top-down DP (simplify state) =====
"""
- Notice that the number of set bits in used_bikes_mask is always equal i_w.
  . If 0 bits are set -> we are handling worker0
  . If 2 bits are set -> we are handling worker2
  . ...
-> Just need 'used_bikes_mask' as state.

- To count number of set bits in an integer (population count, hamming weight):
  + built-in: used_bikes_mask.bit_count() -> fastest
  + Brian Kernighan's algorithm () -> fast, O(set_bits)
  + string conversion: bin(used_bikes_mask).count('1') -> slower, O(total_bits)
"""


def assign_bikes(workers: list[tuple[int, int]], bikes: list[tuple[int, int]]) -> int:
    m, n = len(bikes), len(workers)

    def manhattan_dist(x: tuple[int, int], y: tuple[int, int]) -> int:
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def count_set_bits(x: int) -> int:
        count = 0
        while x:
            x &= x - 1  # clear the least significant set bit
            count += 1
        return count

    @cache
    def dp(used_bikes_mask: int) -> int:
        # i_w = count_set_bits(used_bikes_mask)
        i_w = used_bikes_mask.bit_count()

        if i_w == n:
            return 0

        min_dist = math.inf
        for i_b in range(m):
            if (used_bikes_mask >> i_b) & 1:
                continue
            dist = manhattan_dist(workers[i_w], bikes[i_b])
            new_mask = used_bikes_mask ^ (1 << i_b)
            min_dist = min(min_dist, dist + dp(new_mask))
        return min_dist

    return dp(0)


"""
Complexity:

1. Time complexity: O(m * 2^m)
- Number of DP states: 2^m
- Each state has a loop with m iterations.

2. Space complexity: O(2^m)
- memoization table: O(2^m)
- recursion stack: O(n)
"""


# ===== Approach 3.1: Bottom-up DP =====
# TODO

# ===== Approach 3.2: Bottom-up DP (simplify state) =====
# TODO
