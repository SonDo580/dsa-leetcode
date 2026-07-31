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
- Use backtracking to try all worker-bike pairs.
  States needed:
  . i_w: current worker
  . used_bikes: a set to track used bikes.
  . total_distance: total Manhattan distance with current assignments.
- Base case: 
  . i_w == n -> all workers have been assigned bikes
    -> update min_distance if total_distance < min_distance 
- At each step, try assigning each unused bike to current worker.
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

- Alternative view:
  Number of ways to choose n bikes from m bikes and arrange them in order:
  . mPn = m! / (m - n)! = m * (m - 1) * ... * (m - n + 1) < m^n
   
2. Space complexity: O(n)
- recursion stack: O(n)
- used_bikes_set: O(n) 
  (assign to n workers, reused across 'backtrack' calls)
"""


# ===== Approach 1.2: Backtracking + bitmask =====
# (exceed time limit)
"""
- For each bike, we can either use it or not use it
  -> use integer in range 0 to 2^m - 1 to represent used bikes. 
- ith bike is used if ith bit of mask is set:
  . (mask >> i) & 1 = 1
- flip ith bit of mask to mark ith bike as used/unused:
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
            backtrack(
                i_w + 1,
                used_bikes_mask ^ (1 << i_b),
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
Identify DP:
- There are overlapping sub-problems. For example:
  . assign bike1 to worker1, bike 2 to worker2
  . assign bike2 to worker1, bike 1 to worker2
  . If dist(w1, b1) + dist(w2, b2) = dist(w1, b2) + dist(w2, b1)
    then both cases lead to the same (worker3, used_bikes, total_dist).

Idea:
- Let dp(i_w, used_bikes_mask) be the minimum total distance between 
  each worker and their assigned bike for workers[i_w..n-1], 
  with used_bikes_mask represents bikes assigned to workers[0..i_w-1].
- Result: dp(i_w=0, used_bikes_mask=0).
  . [0..i_w-1] = [0..0-1] = []
    -> no previous workers to assign bikes 
    -> no used bikes
- At each step, try assigning each remaining bike to current worker.
  Accumulate Manhattan distance, mark used bike, and go to next worker.
  . dp(i_w, used_bikes_mask) = min(dist(i_w, i_b) + dp(i_w + 1, next_mask))
- Base case: dp(n, ...) = 0
  . [i_w..n-1] = [n..n-1] = []
    -> no workers remaining
    -> total_distance = 0
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
            next_mask = used_bikes_mask ^ (1 << i_b)
            min_dist = min(min_dist, dist + dp(i_w + 1, next_mask))
        return min_dist

    return dp(0, 0)


"""
Complexity:

1. Time complexity: O(n * m * 2^m)
- Number of DP states: n * 2^m
- Each state has a loop with m iterations.

2. Space complexity: O(n * 2^m)
- cache: O(n * 2^m)
- recursion stack: O(n)
"""


# ===== Approach 2.2: Top-down DP (simplify state) =====
"""
- The number of set bits in used_bikes_mask always equal i_w.
  . If 0 bits are set 
    -> haven't assigned bikes to any worker
    -> handling worker0
  . If 2 bits are set
    -> assigned bikes to worker0 and worker1
    -> handling worker2
  . ...
-> Just need 'used_bikes_mask' as state.

- To count number of set bits in an integer (population count, hamming weight):
  + built-in: used_bikes_mask.bit_count() -> fastest, O(1)
  + Brian Kernighan's algorithm -> fast, O(set_bits)
  + string conversion: bin(used_bikes_mask).count('1') -> slower, O(total_bits)
"""


def assign_bikes(workers: list[tuple[int, int]], bikes: list[tuple[int, int]]) -> int:
    m, n = len(bikes), len(workers)

    def manhattan_dist(x: tuple[int, int], y: tuple[int, int]) -> int:
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def count_set_bits(x: int) -> int:
        count = 0
        while x:
            x &= x - 1  # clear the lowest set bit
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
            next_mask = used_bikes_mask ^ (1 << i_b)
            min_dist = min(min_dist, dist + dp(next_mask))
        return min_dist

    return dp(0)


"""
Complexity:

1. Time complexity: O(m * 2^m)
- Number of DP states: 2^m
- Each state has a loop with m iterations.

2. Space complexity: O(2^m)
- cache: O(2^m)
- recursion stack: O(n) 
  . used_bike_mask increases with each level so i_w go from 0 to n
"""


# ===== Approach 3: Bottom-up DP =====
class Solution:
    def assignBikes(self, workers: list[list[int]], bikes: list[list[int]]) -> int:
        def manhattan_dist(x: tuple[int, int], y: tuple[int, int]) -> int:
            return abs(x[0] - y[0]) + abs(x[1] - y[1])

        m, n = len(bikes), len(workers)
        dp = [math.inf] * (1 << m)  # used_bikes_mask range: [0..2^m-1]

        for mask in range((1 << m) - 1, -1, -1):
            i_w = mask.bit_count()

            if i_w > n:
                continue

            if i_w == n:
                dp[mask] = 0
                continue

            for i_b in range(m):
                if (mask >> i_b) & 1:
                    continue
                dist = manhattan_dist(workers[i_w], bikes[i_b])
                next_mask = mask ^ (1 << i_b)
                dp[mask] = min(dp[mask], dist + dp[next_mask])

        return dp[0]


"""
Complexity:
1. Time complexity: O(m * 2^m)
2. Space complexity: O(2^m) for 'dp'
"""


# ===== Alternative implementation =====
# ======================================
"""
- Let dp(used_bikes_mask) be the minimum total distance between 
  each worker and their assigned bike for workers[0..i_w-1], 
  with used_bikes_mask represents bikes assigned to workers[0..i_w-1].
  -> Handling next worker i_w = count_ones(used_bit_mask)
- Result: min(total distance after assigned bikes for workers[0..n-1])
  . res = min(dp(mask) where count_ones(mask) = i_w = n)
- At each step, try assigning each remaining bike to next worker i_w.
  Accumulate Manhattan distance, mark used bike, and go to the next worker.
  . dp(next_used_bikes_mask) = min(dist(i_w, i_b) + dp(used_bikes_mask))
    (Only if i_w < n. Otherwise there're no remaining workers)
- Base case: dp(0) = 0
  . handling worker i_w = count_ones(mask) = count_ones(0) = 0,
    return result for workers [0..i_w-1] = [0..0-1] = []
    -> total_distance = 0 (no workers to assign bikes)
"""


# === Bottom-up ===
class Solution:
    def assignBikes(self, workers: list[list[int]], bikes: list[list[int]]) -> int:
        def manhattan_dist(x: tuple[int, int], y: tuple[int, int]) -> int:
            return abs(x[0] - y[0]) + abs(x[1] - y[1])

        m, n = len(bikes), len(workers)
        dp = [math.inf] * (1 << m)
        dp[0] = 0

        for mask in range(1 << m):
            i_w = mask.bit_count()
            if i_w >= n:
                continue

            for i_b in range(m):
                if (mask >> i_b) & 1:
                    continue
                dist = manhattan_dist(workers[i_w], bikes[i_b])
                next_mask = mask | (1 << i_b)  # either OR or XOR will work
                dp[next_mask] = min(dp[next_mask], dist + dp[mask])

        return min(dp[mask] for mask in range(1 << m) if mask.bit_count() == n)


"""
Complexity:
1. Time complexity: O(m * 2^m)
- Init 'dp': O(2^m)
- Fill 'dp': O(m * 2^m)
- Find result: O(2^m)

2. Space complexity: O(2^m) for 'dp'
"""


# === Top-down ===
"""
- We are going backward to reach i_w = 0:
  -> dp(used_bikes_mask) = min(dist(i_w-1, i_b) + dp(prev_used_bikes_mask))
     . i_w = count_ones(used_bikes_mask)
     . prev_used_bikes_mask = unset_bit(used_bikes_mask, i_b)
- Meaning: At each state, try each used bike as assigned bike 
           for the last worker that has been assigned bike.
- Why the last worker that has been assigned bike is i_w-1:
  . used_bikes_mask represent used bikes for workers[0..i_w-1]
"""


class Solution:
    def assignBikes(self, workers: list[list[int]], bikes: list[list[int]]) -> int:
        def manhattan_dist(x: tuple[int, int], y: tuple[int, int]) -> int:
            return abs(x[0] - y[0]) + abs(x[1] - y[1])

        m, n = len(bikes), len(workers)

        @cache
        def dp(used_bikes_mask: int) -> int:
            i_w = used_bikes_mask.bit_count()
            if i_w == 0:
                return 0

            min_dist = math.inf
            for i_b in range(m):
                # Try each assigned bike as assigned bike for worker i_w-1
                if (used_bikes_mask >> i_b) & 1:
                    prev_mask = used_bikes_mask ^ (
                        1 << i_b
                    )  # Mark i_b as not used by workers[0..i_w-2]
                    dist = manhattan_dist(workers[i_w - 1], bikes[i_b])
                    min_dist = min(min_dist, dist + dp(prev_mask))

            return min_dist

        return min(dp(mask) for mask in range(1 << m) if mask.bit_count() == n)


"""
Complexity:

1. Time complexity: O(m * 2^m + 2^m) = O(m * 2^m)
- Number of DP states: 2^m
  Each state has a loop with m iterations.
- Iterate through dp(mask) with count_ones(masks) == n: O(2^m)

2. Space complexity: O(2^m)
- cache: O(2^m)
- recursion stack: O(n)
"""