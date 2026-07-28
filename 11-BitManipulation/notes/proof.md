# `n & (n - 1)` set the lowest 1 of n to 0

```
- We can write n and n-1 as:
  . n = (H << (k + 1)) + 2^k
  . n - 1 = (H << (k + 1)) + (2^k - 1)

- Bit representations:
  . n = H 1 0 ... 0
            ^^^^^^^
            k zeros

  . n - 1 = H 0 1 ... 1
                ^^^^^^^
                k ones

- Compute n & (n - 1):
  . result = H  0     0 ... 0
                ^     ^^^^^^^
              unset   k zeros
```

# Negation: `-a = ~(a - 1) = ~a + 1`

```
- Let bit length = k

. ~a + a = 2^k - 1 = -1   (bit representation: k 1's)
  -> ~a + 1 = -a

. ~(a - 1) + (a - 1) = 2^k - 1 = -1
  -> ~(a - 1) = -a
```

# `n & (-n) = n & (~(n - 1))` keep the lowest 1 and set remaining 1's to 0

```
- Bit representations:
  . n = H 1 0 ... 0
            ^^^^^^^
            k zeros

  . n - 1 = H 0 1 ... 1
                ^^^^^^^
                k ones
  . ~(n - 1) = ~H 1 0 ... 0
                    ^^^^^^^
                    k zeros

- Compute n & (~(n - 1)):
  . H & (~H) = 0
  -> result = 0 ... 0   1    0 ... 0
                        ^    ^^^^^^^
                       keep  k zeros
```

# Convert decimal to base X, integer part

- Divide integer part by X until it reaches 0.
  Traversing remainder in **reverse** order gives representation in base X.

```
N = a[k] * X^k + a[k-1] * X^(k-1) + ... + a[1] * X + a[0]
  = X * (a[k] * X^(k-1) + a[k-1] * X^(k-2) + ... + a[1]) + a[0]
-> . N % X = a[0]
   . next_N = a[k] * X^(k-1) + a[k-1] * X^(k-2) + ... + a[1]
- Repeat the process yields remainder a[0], a[1], ... a[k-1], a[k]
  (Stop when next_N = 0).
```

# Convert decimal to base X, fractional part

- Multiply fractional part with X until it reaches 0.
  Traversing the integer part in order gives representation in base X.

```
F is in [0, 1) in base 10.
- Representation in base X:
  . F = d[1] / X + d[2] / X^2 + ... (where d[i] are fractional digits)
- Multiply both side with X:
  . F * X = d[1] + d[2] / X + d[3] / X^3 + ...
  Take integer part: floor(F * X) = d[1]
  -> Repeat the process yields integer parts d[1], d[2], ...
     (Stop when fractional part reaches 0)
```

# De Morgan's law

## `~(a & b) = (~a) | (~b)`

TODO

## `~(a | b) = (~a) & (~b)`

TODO

# Distributive laws

## `(a & b) | c = (a | c) & (b | c)`

TODO

## `(a | b) & c = (a & c) | (b & c)`

TODO

## `(a ^ b) & c = (a & c) ^ (b & c)`

- Algebraic proof _(based on other distributive laws and De Morgan's laws)_

```
. LHS = (a ^ b) & c
  = ((a & ~b) | (~a & b)) & c
  = (a & c & ~b) | (b & c & ~a)

. RHS = (a & c) ^ (b & c)
  = ((a & c) & ~(b & c)) | ((b & c) & ~(a & c))
  = ((a & c) & (~b | ~c)) | ((b & c) & (~a | ~c))
  = ((a & c & ~b) | (a & c & ~c)) | ((b & c & ~a) | (b & c & ~c))
  = ((a & c & ~b) | (a & 0)) | ((b & c & ~a) | (b & 0))
  = ((a & c & ~b) | 0) | ((b & c & ~a) | 0)
  = (a & c & ~b) | (b & c & ~a)

-> LHS = RHS
```

# `x << k` is equivalent to `x * 2^k`

TODO

# Logical right shift is equivalent to `x // 2^k` (x >= 0)

TODO

# Arithmetic right shift is equivalent to `x // 2^k`

TODO
