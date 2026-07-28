"""
Given a 4 x 4 matrix.
Count how many ways to put items such that
there are no adjacent items on the same row.
"""

# === Approach 1 ===
"""
Idea:
- Number of possible placements for each column: 2^4 
  -> Each placement can be represented with an integer in [0..2^4-1].
  -> ith bit = 1 <-> 1 item is in row i of that column. 
- Let representations for 2 adjacent columns be x and y.
  . If x & y == 0, there are no adjacent items on the same row.
"""


def count_ways():
    cnt = 0
    column_placements = 1 << 4
    for i in range(column_placements):
        for j in range(column_placements):
            for k in range(column_placements):
                for l in range(column_placements):
                    if (i & j) == 0 and (j & k) == 0 and (k & l) == 0:
                        cnt += 1
    return cnt


"""
Complexity:
- Let n = matrix dimension (4 in this problem) 

1. Time complexity: O(2^(n^2))
- Number of possible placements for 1 column = 2^n
- Number of nested loop levels = number of rows = n
-> Number of innermost loop iterations: (2^n)^n = 2^(n*n) = 2^(n^2)

2. Space complexity: O(1)
"""


# === Approach 2: Backtracking / Top-down DP ===
"""
- Placement in a row doesn't affect other rows.
  -> . Number of ways to put items on 1 row: row_cnt
     . Number of ways: cnt = row_cnt ^ 4    (power, not XOR)
- Count number of ways to put items on 1 row
  such that there are no adjacent items:
  . Use backtracking. State needed:
    . i: current column
    . prev_used: True if place item in previous column
  . 2 options at each column:
    . Don't place an item there
    . Place an item previous column is empty.
  . Increment count by 1 after considering all columns.

Optimize:
- We can arrive at the same (i, prev_used) from multiple paths
  -> Cache result to avoid recomputation (becomes Top-down DP). 
"""

from functools import cache


def count_ways_v2():
    num_rows = 4
    num_cols = 4

    @cache
    def place(i: int, prev_used: bool) -> int:
        """Number of ways to put items in 1 row starting from column i."""
        if i == num_cols:  # considered all columns
            return 1

        cnt = 0

        # option 1: don't place an item at column i
        cnt += place(i + 1, prev_used=False)

        # option 2: place an item at column i if possible
        if not prev_used:
            cnt += place(i + 1, prev_used=True)

        return cnt

    return place(i=0, prev_used=False) ** num_rows


"""
Complexity:
- Let n = matrix dimension (4 in this problem) 

1. Time complexity: O(n)
- Number of DP states: O(2*n) 
- Work at each state: O(1)

2. Space complexity: O(n) 
- recursion stack: O(n)
- memoization table: O(2*n) = O(n)
"""


# === Approach 3: Bottom-up DP ===
"""
- Let dp[1][i] = number of ways to place items starting from column i 
                 if column i-1 is occupied. 
      dp[0][i] = number of ways to place items starting from column i 
                 if column i-1 is empty.
- Base case: dp[0][n] = dp[1][n] = 1
  (considered all columns <-> 1 valid placement)
- Recurrence:
  . dp[1][i-1] <-> take slot i-2
    -> can only skip slot i-1
    -> dp[1][i-1] = dp[0][i]
  . dp[0][i-1] <-> skip slot i-2
    -> can either take or skip slot i-1
    -> dp[0][i-1] = dp[1][i] + dp[0][i]
- Result: dp[0][0]
  (number of placement starting from column 0, no previous column)
- Recurrence relation is static -> can optimize space.
  . Use 2 variables cnt_true and cnt_false
    to represent dp[1][i] and dp[0][i].
"""


def count_ways_v3():
    num_rows = 4
    num_cols = 4

    cnt_true = cnt_false = 1
    for _ in range(num_cols):  # range(num_cols - 1, -1, -1) is equivalent
        cnt_true, cnt_false = cnt_false, cnt_true + cnt_false

    return cnt_false**num_rows


"""
Complexity:
- Let n = matrix dimension (4 in this problem) 

1. Time complexity: O(n)
2. Space complexity: O(1)
"""


if __name__ == "__main__":
    print(count_ways())
    print(count_ways_v2())
    print(count_ways_v3())
