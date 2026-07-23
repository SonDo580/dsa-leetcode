"""
Find the GCD of 2 positive integers a and b.

The GCD (Greatest Common Divisor) or HCF (Highest Common Factor)
of 2 numbers is the largest number that divides both of them.
"""

# === Approach 1 ===
"""
- Try all values from 1 to min(a, b),
  check which number divides both a and b.
- Iterate in reverse order to break early,
  since we want the largest number.
"""


def gcd_v1(a: int, b: int) -> int:
    assert a > 0 and b > 0

    ans = min(a, b)
    while True:  # guaranteed to break (ans = 1 if both numbers are prime)
        if a % ans == 0 and b % ans == 0:
            break
        ans -= 1

    return ans


"""
Complexity:
1. Time complexity: O(min(a, b))
2. Space complexity: O(1)
"""

# === Approach 2: Euclidean algorithm by subtraction ===
"""
- If a == b, GCD(a, b) = a = b
- If a > b, GCD(a, b) = GCD(a - b, b)
  Repeat the process until reaching base case.

  
=== Proof ===
- Let d1 = gcd(a, b), 
      d2 = gcd(a - b, b)  (a > b)

. a = k1*d1
  b = k2*d1
  a - b = (k1 - k2)*d1
  -> d1 is a common divisor of (a - b) and b.
. Since d2 is the greatest common divisor of (a - b) and b,
  any common divisor of (a - b) and b must divide d2.
  -> d2 % d1 == 0       (1)

. a - b = l1*d2
  b = l2*d2
  (a - b) + b = a = (l1 + l2)*d2
  -> d2 is a common divisor of a and b.
. Since d1 is the greatest common divisor of a and b,
  any common divisor of a and b must divide d1.
  -> d1 % d2 == 0       (2)

- From (1) and (2): d1 = d2
  -> gcd(a, b) = gcd(a - b, b)
"""


def gcd_v2(a: int, b: int) -> int:
    assert a > 0 and b > 0
    if a == b:
        return a
    if a > b:
        return gcd_v2(a - b, b)
    else:
        return gcd_v2(a, b - a)


def gcd_v2_iter(a: int, b: int) -> int:
    assert a > 0 and b > 0
    while a != b:
        a, b = abs(a - b), min(a, b)
    return a


"""
Complexity:
- Worst case: 1 number is very large (N), the other is 1
  -> subtract (N-1) times until a = b = 1

1. Time complexity: O(max(a, b))

2. Space complexity: 
- recursive approach: O(max(a, b))
- iterative approach: O(1)
"""


# === Approach 3: Euclidean algorithm: check divisibility ===
"""
- Optimize approach 2: break early if 1 number divide the other.
"""


def gcd_v3(a: int, b: int) -> int:
    assert a > 0 and b > 0
    if a == b:
        return a

    if a > b:
        if a % b == 0:
            return b
        return gcd_v3(a - b, b)

    if b % a == 0:
        return a
    return gcd_v3(a, b - a)


def gcd_v3_iter(a: int, b: int) -> int:
    assert a > 0 and b > 0
    while a != b:
        if a > b:
            if a % b == 0:
                return b
            a, b = a - b, b
        else:
            if b % a == 0:
                return a
            a, b = a, b - a
    return a


"""
Complexity:
- Worst case: 1 number is very large and not divisible by 2, the other is 2
- Example: a = 1001, b = 2
  . 1001 % 2 != 0 -> a = 1001 - 2 = 999
  . 999 % 2 != 0 -> a = 999 - 2 = 997
  . ...
  (N = 2*k + 1 -> subtract a by 2 k = N//2 times until a = 1,
   then next_b = b - a 2 - 1 = 1 = a)

1. Time complexity: O(max(a, b))

2. Space complexity:
- recursive approach: O(max(a, b))
- iterative approach: O(1)
"""


# === Approach 4: Euclidean algorithm: check remainder ===
"""
- If a % b == 0, return b
- GCD(a, b) = GCD(b, a % b)


=== Proof ===
. a % b = r     
  -> a = q*b + r
  -> r = a - q*b    (0 <= r < b)

- Let d be a common divisor of a and b
  -> a = k1*d
     b = k2*d
  -> r = a - q*b = (k1 - q*k2)*d
  -> r % d == 0
  -> All common divisors of a and b divides r   (1)

- Let d' be a common divisor of b and r
  -> b = l1*d'
     r = l2*d'
  -> a = q*b + r = (l1*q + l2)*d'
  -> a % d' == 0
  -> All common divisors of b and r divides a   (2)

- From (1) and (2)
  -> CD_set(a, b) = CD_set(b, r)
  -> GCD(a, b) = GCD(b, r)
"""


def gcd_v4(a: int, b: int) -> int:
    return a if b == 0 else gcd_v4(b, a % b)


def gcd_v4_iter(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


"""
Complexity:

1. Time complexity: O(log(min(a, b)))
- Worst case: input are consecutive Fibonacci numbers

2. Space complexity:
- recursive approach: O(log(min(a, b)))
- iterative approach: O(1)


=== Time complexity in details ===
- Let a >= b > 0
      r = a % b -> (0 <= r < b)
 
- Iteration i params: a, b
  . If b <= a/2
    -> r < b <= a/2
    -> r < a/2
  . If b > a/2
    -> b fits into a exactly once
    -> r = a - b*1 = a - b
    -> r < a - a/2
    -> r < a/2
  Iteration i+1 params: b, r
  Iteration i+2 params: r, b % r
  -> Input size is cut more than half every 2 iterations
  -> The algorithm takes at most 2*log2(a) steps (reduce a to 1)
  -> T = O(log(a))

- Even when a is larger, it is reduced to < b in 1 step.
  -> T can be considered O(log(min(a, b)))


=== Worst case: input are consecutive Fibonacci numbers ===
Proof: TODO
"""


if __name__ == "__main__":
    for gcd_fn in [
        gcd_v1,
        gcd_v2,
        gcd_v2_iter,
        gcd_v3,
        gcd_v3_iter,
        gcd_v4,
        gcd_v4_iter,
    ]:
        assert gcd_fn(20, 28) == gcd_fn(28, 20) == 4
        assert gcd_fn(17, 19) == gcd_fn(19, 17) == 1
