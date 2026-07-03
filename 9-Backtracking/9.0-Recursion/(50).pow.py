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
