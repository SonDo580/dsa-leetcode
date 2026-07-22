# Modular Arithmetic

1. **Addition:**

- Variation 1: `(a + b) mod n = ((a mod n) + (b mod n)) mod n`

```
. c = a mod n -> a = k*n + c
. d = b mod n -> b = l*n + d
. (a + b) mod n
   = ((k + l)\*n + c + d) mod n
   = (c + d) mod n
   = ((a mod n) + (b mod n)) mod n
```

- Variation 2 (most used): `(a + b) mod n = ((a mod n) + b) mod n`

```
. r = a mod n -> a = k*n + r
. (a + b) mod n
   = (k*n + r + b) mod n
   = (r + b) mod n
   = ((a mod n) + b) mod n
```

2. **Multiplication:**

- Variation 1: `a*b mod n = (a mod n)*(b mod n) mod n`

```
. c = a mod n -> a = k*n + c
. d = b mod n -> b = l*n + d
. a*b mod n
   = (k*l*n + (k*d + l*c)n + c*d) mod n
   = c*d mod n
   = (a mod n)*(b mod n) mod n
```

- Variation 2 (most used): `a*b mod n = (a mod n)*b mod n`

```
. r = a mod n -> a = k*n + r
. a*b mod n
   = (b*k*n + b*r) mod n
   = b*r mod n
   = (a mod n)*b mod n
```

3. **Exponentiation:**

_(here '^' denotes power, not bitwise XOR)_

`a^b mod n = (a mod n)^b mod n`

```
. c = a mod n -> a = k*n + c
. a^b mod n = (k*n + c)^b mod n

- Using binominal theorem:
  (k*n + c)^b
  = sum(bCi * (k*n)^(b-i) *c^i)     (i in [0..b])
  = (k*n)^b + b * (k*n)^(b-1) * c + ... + b * (k*n) * c^(b-1) + c^b

- All terms except c^b have factor k*n
-> a^b mod n
   = (k*n + c)^b mod n
   = c^b mod n
   = (a mod n)^b mod n
```

4. **Subtraction:**

- Variation 1: `(a - b) mod n = ((a mod n) - (b mod n)) mod n`

```
. c = a mod n -> a = k*n + c
. d = b mod n -> b = l*n + d
. (a - b) mod n
   = ((k - l)*n + (c - d)) mod n
   = (c - d + n) mod n
   = ((a mod n) - (b mod n) + n) mod n
```

- Variation 2 (most used): `(a - b) mod n = ((a mod n) - b) mod n`

```
. r = a mod n -> a = k*n + r
. (a - b) mod n
   = (k*n + r - b) mod n
   = (r - b) mod n     (+n to normalize into range [0, n))
   = ((a mod n) - b) mod n
```

- **In programming**, add n to normalize result into range `[0, n)`: `(a - b) mod n = ((a mod n) - b + n) mod n`

5. **Division**

- **Modular inverse**: `b*inv(b) mod n = 1`
- **Division**: `a/b mod n = a*inv(b) mod n = ((a mod n) * inv(b)) mod n`
- Find `inv(b)`: TODO

## Properties

1. **Distribution over addition:**

`a*(b + c) mod n = ((a*b mod n) + (a*c mod n)) mod n`

```
. a*(b + c) mod n = (a*b + a*c) mod n
= ((a*b mod n) + (a*c mod n)) mod n    (by addition rule)
```

2. **Congruence Idempotence:**

`(x mod n) mod n = x mod n`

```
. r = x mod n
. 0 <= r < n
  -> r mod n = r
  -> (x mod n) mod n = r mod n = r
```

3. **Identity elements:**

- Additive identify (0): `(a + 0) mod n = a mod n`
- Multiplicative identify (1): `(a * 1) mod n = a mod n`

## Applications

- Prevent overflow when dealing with large number
- ...
