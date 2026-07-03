"""
https://leetcode.com/problems/powx-n/

Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).
"""

# === 1) Exceed time limit ===
"""
Idea: recursion
- F(i) = x^i -> final answer: F(n)
- n = 0 -> F(0) = 1 (base case)
  n < 0 -> F(n) = 1/F(-n)
  n > 0 -> F(n) = F(n - 1) * x
"""


def my_pow(x: float, n: int) -> float:
    if n == 0:
        return 1
    if n < 0:
        return 1 / my_pow(x, -n)
    return x * my_pow(x, n - 1)


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(n)
"""


# === 2) Improvement ===
"""
- Reduce to the base case faster.
- (Roughly) x^i = (x^(i/2))^2 -> try to cut in half each time.
- i > 0:
  . i is odd -> i = 2*(i // 2) + 1
    -> F(i) = F(i // 2) * F(i // 2) * x
  . i is even -> i = 2*(i // 2)
    -> F(i) = F(i // 2) * F(i // 2)
"""


def my_pow(x: float, n: int) -> float:
    if n == 0:
        return 1
    if n < 0:
        return 1 / my_pow(x, -n)

    half_exp = my_pow(x, n // 2)
    if n % 2 == 1:
        return half_exp * half_exp * x
    return half_exp * half_exp


"""
Complexity:
- Let k be number of splits until n == 0.
- n is halved each time: n -> n // 2 -> ... -> 0.
- 2^k = n -> k = log2(n).

1. Time complexity: O(log(n))
2. Space complexity: O(log(n))
"""


# === Iterative approach (optimize space) ===
def my_pow(x: float, n: int) -> float:
    if n == 0:
        return 1
    if n < 0:
        return 1 / my_pow(x, -n)

    i = 1
    remain_n = n
    ans = 1
    curr = x

    while i < remain_n:
        if i * 2 > remain_n:
            ans *= curr

            remain_n -= i
            i = 1
            curr = x
        else:
            i *= 2
            curr *= curr

    ans *= curr
    return ans


"""
Complexity:

1. Time complexity: 
- Best case: O(log(n))
  . when n = 2^m
  . i is doubled each time until it reaches n
    - number of doublings needed: k = log2(n)
- Worst case: O((log n)^2)
  . when n = 2^m - 1 (binary representation = all 1's)
    (example: 1, 3, 7, 15, 31, ...)

2. Space complexity: O(1)


=== Time complexity - worst case in detailed ===
- Let's analyze a single segment of the while loop
  + Initially: 
    . k = n = 2^m - 1
    . i = 1 
  + Double i in each iteration as long as i * 2 <= k
    . i: 1 -> 2 -> ... -> 2^(m - 1)
      (takes m - 1 iterations)
  + On the next iteration, i * 2 = 2^m > k 
    -> reset (1 iteration)
    . k_new = k - i = (2^m - 1) - 2^(m-1) = 2^(m-1) - 1
      (same form, shifted right by 1 bit)
    . i = 1
=> Total iterations for this segment: m

- Consider the entire execution:
  . segment 1: k = 2^m - 1; takes m iterations
  . segment 2: k = 2^(m-1) - 1; takes m - 1 iterations
  . ...
  . segment m-1: k = 2^2 - 1 = 3; takes 2 iterations
  . at this point: k = 2^1 - 1 = 1 = i -> exit while loop
=> Sum up iterations spent in each segment
   . T(n) = m + (m - 1) + ... + 2 = m * (m + 1) / 2 - 1
          = O(m^2)

- Express T(n) in terms of n:
  . n = 2^m - 1 -> m = log2(n + 1)
  . T(n) = O(m^2) = O(log2(n + 1)^2) = O((log n)^2)
"""