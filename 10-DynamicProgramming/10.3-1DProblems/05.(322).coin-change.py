"""
https://leetcode.com/problems/coin-change/

You are given an integer array 'coins' representing coins of different denominations
and an integer 'amount' representing a total amount of money.

Return the fewest number of coins that you need to make up that amount.
If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.
"""

# ***** FAILED ATTEMPTS *****
# ***************************

# ===== 1) 1st attempt (wrong) =====
"""
- To use the minimum number of coins,
  we should use the bigger coins as much as possible (being greedy).
- We can use backtracking, starting from the biggest coin.
  Try to use number of that coin from (amount // value) to 0.
- For each option, calculate the remaining amount.
  Then move to the next biggest coin.
- Base case for backtrack call:
  + amount = 0 -> don't need any coin (return 0)
  + used all coins but remaining > 0 -> return -1
- Return right away when we found a valid solution.

=> Flaws:
- Trying to use the biggest coins as much as possible may not lead to
  the minimum number of coins used overall.
- Example: coins = [10, 6, 1], amount = 12
  + The optimal solution: use 2 coins of 6.
  + Our approach:
    . start with coin 10 -> use 12 // 10 = 1 coin; remaining = 2
    . move to coin 6 -> use 2 // 6 = 0 coin; remaining = 2
    . move to coin 1 -> use 2 // 1 = 2 coin; remaining = 0
    => use 3 coins in total.
"""


# ===== 2) 2nd attempt (exceed time limit) =====
"""
- Also use backtracking like in first attempt.
- However, we will explore all valid combinations, 
  then take the minimum.
"""
import math


def coin_change(coins: list[int], amount: int) -> int:
    def backtrack(i: int, remaining_amount: int) -> int:
        """
        Returns the minimum number of coins to make up remaining_amount,
        using coins from coins[i:].
        """
        # Don't need any coin if amount = 0
        if remaining_amount == 0:
            return 0

        # Used all coins but remaining > 0
        if i == len(coins):
            return -1

        coin = coins[i]
        min_total_num = math.inf
        for num in range(remaining_amount // coin, -1, -1):
            remaining_num = backtrack(i + 1, remaining_amount - num * coin)
            if remaining_num != -1:
                min_total_num = min(min_total_num, num + remaining_num)

        return -1 if min_total_num == math.inf else min_total_num

    return backtrack(0, amount)


"""
Complexity:
- Let n = len(coins) (number of coin types)

1. Time complexity: O(amount^n)
- The recursion depth is n (number of coin types).
- For each coin, we have a loop that runs upto 'amount / coin' times.
  In the worst case (coin has value 1), that is 'amount'.
-> Total: nesting the loops n times leads to O(amount^n)

2. Space complexity: O(n) for the recursion stack
"""


# ===== 3) Top-down DP v0 (exceed time limit) =====
"""
(Optimize 2nd attempt with memoization)

Identify DP problem:
- There are overlapping sub-problems:
  . At each step, we try all possible counts of the current coin.
    Each choice reduces remaining amount differently.
  . But eventually, different combinations of counts can lead to the same state
    (same next coin index and remaining amount).
- Example: coins = [10, 5, 2], amount = 20
  . use 1*10 + 0*5 -> next_coin = 2, remaining_amount = 10
  . use 0*10 + 2*5 -> next_coin = 2, remaining_amount = 10
"""
from functools import cache


def coin_change(coins: list[int], amount: int) -> int:
    @cache
    def dp(i: int, remaining_amount: int) -> int:
        if remaining_amount == 0:
            return 0

        if i == len(coins):
            return -1

        coin = coins[i]
        min_total_num: int = math.inf
        for num in range(remaining_amount // coin + 1):
            remaining_num = dp(i + 1, remaining_amount - num * coin)
            if remaining_num != -1:
                min_total_num = min(min_total_num, num + remaining_num)

        return -1 if min_total_num == math.inf else min_total_num

    return dp(0, amount)


"""
Complexity:

1. Time complexity: O(n * amount^2)
- Number of DP states: 
  . there are (n * amount) combinations of (i, remaining_amount)
- Work per DP state: O(amount)
  . each 'dp' call has a for loop that runs remaining_amount // coin times.
    -> worst case: remaining amount = amount, coin = 1
-> total: O((n * amount) * amount) = O(n * amount^2)
    
2. Space complexity: O(n * amount)
- memoization table: O(n * amount)
- recursion stack: O(n)
"""


# ***** WORKED SOLUTIONS *****
# ****************************

# ===== 4.1) Top-down DP v1 =====
"""
- Each step only decides whether to take or skip 1 coin of type coins[i].
  Pick the option that leads to less number of total coins.
"""


def coin_change(coins: list[int], amount: int) -> int:
    @cache
    def dp(i: int, remaining_amount: int) -> int:
        if remaining_amount == 0:
            return 0

        if i == len(coins):
            # infinity will "bubble up" if there're no valid solutions
            return math.inf

        # Option 1: skip this coin
        skip = dp(i + 1, remaining_amount)

        # Option 2: take this coin
        # . stay at the same i if possible since we have unlimited amount of coins
        take = math.inf
        if remaining_amount >= coins[i]:
            take = 1 + dp(i, remaining_amount - coins[i])

        return min(take, skip)

    min_count = dp(0, amount)
    return -1 if min_count == math.inf else min_count


"""
Complexity:

1. Time complexity: O(n * amount)
- Number of DP states: 
  . there are (n * amount) combinations of (i, remaining_amount)
- Work per DP state: O(1)
-> total: O(n * amount)
    
2. Space complexity: O(n * amount)
- memoization table: O(n * amount)
- recursion stack: O(n + amount)
-> total: O(n * amount + n + amount) = O(n * amount)
"""


# ===== Compare DP v0 and v1 =====
"""
- Both go through the same set of DP states.
  Although the results are cache, v0 revisits each state more times,
  which causes overhead.
- Let's analyze the work for the ith coin with value 1, remaining amount A.
  + v0:
    . compute dp(i, A) -> run the loop A times.
    . compute dp(i, A - 1) -> run the loop A - 1 times.
    . ...
    . compute dp(i, 0) -> run the loop 0 times.
    -> total: A * (A + 1) / 2 = O(A^2)
  + v1:
    . compute dp(i, A) -> 2 operations (skip or take).
    . compute dp(i, A - 1) -> 2 operations.
    . ...
    . compute dp(i, 0) -> 2 operations.
    -> total: 2 * A = O(A)
"""


# ===== 4.2) Bottom-up DP v1 =====
def coin_change(coins: list[int], amount: int) -> int:
    n = len(coins)
    dp = [[math.inf] * (amount + 1) for _ in range(n)]

    for i in range(n - 1, -1, -1):
        dp[i][0] = 0
        for remaining_amount in range(1, amount + 1):
            skip = take = math.inf
            if i < n - 1:
                skip = dp[i + 1][remaining_amount]
            if remaining_amount >= coins[i]:
                take = 1 + dp[i][remaining_amount - coins[i]]
            dp[i][remaining_amount] = min(skip, take)

    return -1 if dp[0][amount] == math.inf else dp[0][amount]


"""
Complexity:

1. Time complexity: O(n * amount)
- Outer loop: O(n) iterations.
- Inner loop: O(amount) iterations, each cost O(1).

2. Space complexity: O(n * amount) for 'dp'
"""


# ===== 5.1) Top-down DP v2 =====
"""
- Let dp(amount) be the minimum number of coins we need
  to exchange 'amount' money.
- At each step, try using any coin and see which one leads to the optimal solution.
-> Recurrence relation:
   . dp(amount) = min(1 + dp(amount - coin) for coin in coins)
- Base case: dp(0) = 0
"""


def coin_change(coins: list[int], amount: int) -> int:
    @cache
    def dp(amount: int) -> int:
        if amount == 0:
            return 0

        min_total_num = math.inf
        for coin in coins:
            if amount >= coin:
                min_total_num = min(min_total_num, 1 + dp(amount - coin))
        return min_total_num

    min_count = dp(amount)
    return -1 if min_count == math.inf else min_count


"""
Complexity:

1. Time complexity: O(n * amount)
- Number of DP states: O(amount)
- Work per DP state: O(n)
    
2. Space complexity: O(amount)
- memoization table: O(amount)
- recursion stack: O(amount)
"""


# ===== 5.2) Bottom-up DP v2 =====
def coin_change(coins: list[int], amount: int) -> int:
    dp = [math.inf] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for coin in coins:
            if a >= coin:
                dp[a] = min(dp[a], 1 + dp[a - coin])

    return -1 if dp[amount] == math.inf else dp[amount]


"""
Complexity:

1. Time complexity: O(n * amount)
- Outer loop: O(amount) iterations.
- Inner loop: O(n) iterations, each cost O(1).

2. Space complexity: O(amount) for 'dp'
"""
