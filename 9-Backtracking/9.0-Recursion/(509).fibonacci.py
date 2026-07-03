"""
https://leetcode.com/problems/fibonacci-number/

The Fibonacci numbers, commonly denoted F(n) form a sequence,
called the Fibonacci sequence,
such that each number is the sum of the two preceding ones,
starting from 0 and 1. That is,

. F(0) = 0, F(1) = 1
. F(n) = F(n - 1) + F(n - 2), for n > 1.

Given n, calculate F(n).
"""


# === 1) Naive recursion ===
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


"""
Complexity:

1. Time complexity: O(2^n)
- Recursion depth: O(n)
- Each call splits 2 more calls

2. Space complexity: O(n) for recursion stack
"""

# === 2) Cache result (Top-down DP) ===
"""
- Each problem is re-calculated multiple times
  -> cache result to avoid recomputation.
"""
from functools import cache


@cache
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


"""
Complexity:
1. Time complexity: O(n) (each state is computed once)
2. Space complexity: O(n) for memoization table & recursion stack
"""


# === 3) Iterative approach (Bottom-up DP with space-optimized) ===
def fib(n: int) -> int:
    if n <= 1:
        return n

    prev2 = 0
    prev1 = 1
    for _ in range(2, n + 1):
        prev1, prev2 = prev1 + prev2, prev1
    return prev1


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""

# === 4) Matrix exponentiation ===
"""
- We want to express state transition using a fixed matrix A
- For Fibonacci:
  . current state vector: 
    X(n) = | F(n)   |
           | F(n-1) |
  . previous state vector:
    X(n-1) = | F(n-1) |
             | F(n-2) |

- Find 2 x 2 matrix A such that X(n) = A x X(n-1)
  | F(n)   | = | a11 a12 | x | F(n-1) |
  | F(n-1) |   | a21 a22 |   | F(n-2) |
             = | a11 * F(n-1) + a12 * F(n-2) |
               | a21 * F(n-1) + a22 * F(n-2) |
  . F(n) = F(n-1) + F(n-2) -> a11 = a12 = 1
  . F(n-1) = F(n-1) -> a21 = 1, a22 = 0
=> A = | 1 1 |
       | 1 0 |

- Unroll to the base case:
  . X(n) = A x X(n - 1) = A^2 x X(n - 2) = ... = A^(n-1) x X(1)

- Base case:
X[1] = | F(1) | = | 1 |
       | F(0) |   | 0 |

- Compute A^p: halve p each time to reduce to base case faster
  . p is even: A^p = A^(p/2) x A^(p/2)
  . p is odd: A^p = A^(p//2) x A^(p//2) x A
"""


# === Some linear algebra ===
"""
Matrix multiplication: A x B = C
- Condition: num_cols_A = num_rows_B
  C: num_rows_A x num_cols_B matrix
- C[i,j] = A[i] . B[j]
  (dot product of row vector A[i] and column vector B[j])
"""

TwoByTwoMatrix = tuple[tuple[int, int], tuple[int, int]]


def fib(n: int) -> int:
    def mat_mul(A: TwoByTwoMatrix, B: TwoByTwoMatrix) -> TwoByTwoMatrix:
        """
        | a11 a12 | x | b11 b12 | = | a11*b11+a12*b21 a11*b12+a12*b22 |
        | a21 a22 |   | b21 b22 |   | a21*b11+a22*b21 a21*b12+a22*b22 |
        """
        return (
            (
                A[0][0] * B[0][0] + A[0][1] * B[1][0],
                A[0][0] * B[0][1] + A[0][1] * B[1][1],
            ),
            (
                A[1][0] * B[0][0] + A[1][1] * B[1][0],
                A[1][0] * B[0][1] + A[1][1] * B[1][1],
            ),
        )

    def mat_pow(A: TwoByTwoMatrix, p: int) -> TwoByTwoMatrix:
        if p == 0:
            return ((1, 0), (0, 1))  # identity matrix
        if p == 1:
            return A

        B = mat_pow(A, p >> 1)  # A^(p // 2)
        if p & 1:  # p % 2 == 1
            return mat_mul(mat_mul(B, B), A)
        return mat_mul(B, B)

    if n <= 1:
        return n

    # A^(n-1)
    A = mat_pow(((1, 1), (1, 0)), n - 1)

    # . X(n) = A^(n-1) x X(1)
    # . | F(n)   | = | a11 a12 | x | 1 | = | a11*1 + a12*0 | = | a11 |
    #   | F(n-1) |   | a21 a22 |   | 0 |   | a21*1 + a22*0 |   | a21 |
    # -> F(n) = a11
    return A[0][0]


"""
Complexity:
- Let k be number of splits until p == 0
  p is halved each time: n -> n // 2 -> ... -> 0
  2^k = p -> k = log2(n)

1. Time complexity: O(log(n))
2. Space complexity: O(log(n))
"""
