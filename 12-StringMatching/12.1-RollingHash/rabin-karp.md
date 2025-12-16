# Problem

Determine if a string `pattern` appears inside a string `text`.

- Let m = length of `pattern`, n = length of `text`.

## Brute-force

- From each position in `text`, compare the next m characters with `pattern`.
- Stop early on mismatch.

Time complexity: O(m \* n)

## Hashing

- Convert `pattern` and each m-length window of `text` to numeric values (hashes).
- Only perform characters check if the hashes match.

**Requirements for the hash function:**

- Rolling hash: can be update in O(1) time when sliding the window.
- Hashes mismatch -> definite non-match.
- Hashes match -> very probable match.
  _(if there are many false positive, performance would degrade to O(m \* n) like brute-force)_

## Rabin-Karp algorithm

1. **Hash formula**

```
hash(s) = (s[0]*p^(n-1) + s[1]*p^(n-2) + ... + s[n - 1]*p^0) % mod
```

where:

- s[i] is the numeric value of the ith character
- p is a small base (prime number, commonly 31 or 37)
- `mod` is a large prime number (like 1e9 + 7) to avoid overflow and reduce hash collisions.

2. **Recurrence relation**

- Let the window size be L.
- Hash of the window [i..i+L-1]:

```
hash(s[i..i+L-1]) = s[i]*p^(L-1) + s[i+1]*p^(L-2) + ... + s[i+L-1]*p^0
```

- Slide the window to the right ([i+1..L]):

```
hash(s[i+1..i+L])
= s[i+1]*p^(L-1) + s[i+2]*p^(L-2) + ... + s[i+L]*p^0
= p * (s[i+1]*p^(L-2) + ... + s[i+L-1]*p^0) + s[i+L]
= p * (hash(s[i..i+L-1]) - s[i]*p^(L-1)) + s[i+L]
```

- To avoid overflow:

```
hash(s[i+1..i+L]) = (p*(hash(s[i..i+L-1]) - s[i]*p^(L-1)) + s[i+L]) % q
```

- `p^(L-1)` can also overflow -> precompute `power = p^(L-1) % q`:

```
. base: p^0 = 1
. recurrence: p^i % q = (p^(i-1) * p) % q = ((p^(i-1) % q) * p) % q

-> Then:
hash(s[i+1..i+L]) = (p*(hash(s[i..i+L-1]) - s[i]*power) + s[i+L]) % q
```

- The result can become negative (due to `-s[i]*power`) -> add `q` to normalize into the range `[0, q - 1]`.

- Calculate hash for the first window (no shrink left):

```
hash(s) = (s[0]*p^(n-1) + s[1]*p^(n-2) + ... + s[n-1]*p^0) % q

hash(s[0..0]) = s[0]*p^0 % q = s[0] % q
hash(s[0..i]) = (s[0]*p^i + s[1]*p^(i-1) + ... + s[i]*p^0) % q
hash(s[0..i+1]) = (s[0]* p^(i+1) + s[1]*p^i + ... + s[i]*p^1 + s[i+1]*p^0) % q

-> Recurrence relation: hash(s[0..i+1]) = (p*hash(s[0..i]) + s[i+1]) % q
```

3. **Algorithm**

- Pick p and q.
- Compute the hashes for `pattern` and the first window.
- Compare the hashes:
  - If they match, perform characters check.
  - Otherwise, slide the window and repeat.

4. **Hash formula intuition**

-- **Let's try a simple hash function:** assign integer values for characters and sum them.

```
hash(s) = s[0] + s[1] + ... + s[n - 1]
```

This function has a very high chance of collision:

- permutations produce the same hash:

```
hash('abc') = 1 + 2 + 3 = 6
hash('bca') = 2 + 3 + 1 = 6
```

- different-length strings can produce the same hash:

```
hash('abc') = 1 + 2 + 3 = 6
hash('cc') = 3 + 3 = 6
hash('abba') = 1 + 2 + 2 + 1 = 6
```

-- **Let's weight the characters by their positions:**

```
hash(s) = s[0]*0 + s[1]*1 + ... + s[n - 1]*(n - 1)
```

This solves permutations collisions.
But linear combinations can still collide easily:

- first character is ignored:

```
hash('abcd') = 1*0 + 2*1 + 3*2 + 4*3 = 20
hash('bbcd') = 2*0 + 2*1 + 3*2 + 4*3 = 20
```

- increase in 1 position can be canceled by decrease in another position:

```
hash('abcde') = 1*0 + 2*1 + 3*2 + 4*3 + 5*4 = 40
hash('abadf') = 1*0 + 2*1 + (3 - 2)*2 + 4*3 + (5 + 1)*4 = 40
```

-- **Let's use exponential weights:**

```
hash(s) = s[0]*p^0 + s[1]*p^1 + ... + s[n-1]*p^(n-1)
```

- now every character matters (don't ignore the first character like with linear weights)
- make it harder to compensate changes.

-- **`rolling hash` with increasing exponential weights:**

- Let the window size be L.
- Hash of window [i..i+L-1]:

```
hash(s[i..i+L-1]) = s[i]*p^i + s[i+1]*p^(i+1) + ... + s[i+L-1]*p^(i+L-1)
```

- Hash of next window [i+1..L]:

```
hash(s[i+1..i+L])
= s[i+1]*p^i + s[i+2]*p^(i+1) + ... + s[i+L]*p^(i+L-1)
= (s[i+1]*p^(i + 1) + ... + s[i+L-1]*p^(i+L-1)) / p + s[i+L]*p^(i+L-1)
= (hash(s[i..i+L-1]) - s[i]*p^i) / p + s[i+L]*p^(i+L-1)
```

-- **`rolling hash` with decreasing exponential weights:**

- Hash of window [i..i+L-1]:

```
hash(s[i..i+L-1]) = s[i]*p^(L-1) + s[i+1]*p^(L-2) + ... + s[i+L-1]*p^0
```

- Hash of next window [i+1..L]:

```
hash(s[i+1..i+L])
= s[i+1]*p^(L-1) + s[i+2]*p^(L-2) + ... + s[i+L]*p^0
= p * (s[i+1]*p^(L-2) + ... + s[i+L-1]*p^0) + s[i+L]
= (hash(s[i..i+L-1]) - s[i]*p^(L-1)) * p + s[i+L]
```

-- **Compare `rolling hash` formulas:**

```
increasing exponents (I)
hash(s[i+1..i+L]) = (hash(s[i..i+L-1]) - s[i]*p^i) / p + s[i+L]*p^(i+L-1)

decreasing exponents (D)
hash(s[i+1..i+L]) = (hash(s[i..i+L-1]) - s[i]*p^(L-1)) * p + s[i+L]
```

- Formula (I) needs p^i and p^(i+L-1), both must be recomputed every time we slide the window (since i changes). Formula D only needs p^(L-1), which is computed once.
- Later on we need to perform modulo operation. Formula (I) has division by p, which under modulo requires computing a modular inverse. With formula (D), compute modular addition/multiplication is straightforward.
- => **Use decreasing exponential weights.**

-- **To avoid overflow, mod the result:**

```
hash(s) = (s[0]*p^(n-1) + s[1]*p^(n-2) + ... + s[n-1]*p^0) % q
```

- to reduce collisions, `q` should be a large prime number (like 1e9 + 7)

-- **Why normalize the rolling hash result into the range [0, q - 1]:**

- While calculating hash of the first window:

```
hash(s[0..i+1]) = (p*hash(s[0..i]) + s[i+1]) % q
-> this never goes negative
```

- Recurrence relation to calculate hash for later windows:

```
hash(s[i+1..i+L]) = (p*(hash(s[i..i+L-1]) - s[i]*power) + s[i+L]) % q
-> this can become negative due to `-s[i]*power`
```

- If we don't normalize result, an early occurrence of window X can have positive hash value while a later occurrence have negative hash value, which violates a hash function requirements _(different hash values -> 100% not match)_.

- Why the % operation can be negative: Most programming languages define `%` using truncated division (round towards 0), so the remainder keeps the sign of the dividend.

```
-5 = 3*(-2) + 1   -> -5 mod 3 = 1 (Euclidean remainder, what we want)
-5 = 3*(-1) - 2   -> -5 % 3 = -2 (result in programs)
```

## Modular arithmetic used

1. **Addition/Multiplication**

```
(a + b) % q = ((a % q) + (b % q)) % q
(a * b) % q = ((a % q) * (b % q)) % q
```

2. **Subtraction**

```
(a - b) % q = ((a % q) - (b % q)) % q
```

_(For Euclidean remainder, add q if result < 0)_

3. **Division**

```
(b * inv(b)) % q = 1  -> inv(b) is the modular inverse of b
(a / b) % q = (a * inv(b)) % q
```
