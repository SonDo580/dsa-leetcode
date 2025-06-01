# Modular Arithmetic

1. **Addition:**

```
(a + b) mod n = ((a mod n) + (b mod n)) mod n
```

- Proof:

```
c = a mod n => a = kn + c
d = b mod n => b = ln + d
(a + b) mod n = ((k + l)n + c + d) mod n
              = (c + d) mod n
              = ((a mod n) + (b mod n)) mod n
```

2. **Multiplication:**

```
ab mod n = (a mod n).(b mod n) mod n
```

- Proof:

```
c = a mod n => a = kn + c
d = b mod n => b = ln + d
ab mod n = (kln + (kd + lc)n + cd) mod n
         = cd mod n
         = (a mod n).(b mod n) mod n
```

3. **Exponentiation:**

```
a^b mod n = (a mod n)^b mod n
```

- Proof:

```
c = a mod n => a = kn + c
a^b mod n = (kn + c)^b mod n
- Using binominal theorem:
  (kn + c)^b = sum(i:0->b):(bCi).(kn)^(b-i).c^i
             = (kn)^b + b(kn)^(b-1) + ... + b(kn)c^(b-1) + c^b
=> All terms except c^b have a factor of kn, hence divisible by n
=> a^b mod n = (kn + c)^b mod n
             = c^b mod n
             = (a mod n)^b mod n
```

4. **Inverse:**

**...Others...**

## Variations

1. **Addition**

```
(a + b) mod n = ((a mod n) + b) mod n

- General case: 
(a1 + a2 + ... + an) mod n = (((a1 mod n) + a2) mod n + ... + an) mod n
```

- Proof:

```
r = a mod n => a = kn + r
(a + b) mod n = (kn + r + b) mod n
         = (r + b) mod n
         = ((a mod n) + b) mod n

- Apply to general case:
  (a1 + a2 + ... + an) mod n 
= ((a1 + a2 + ... + a(n-1)) mod n + an) mod n
= ...
= ((((a1 mod n) + a2) mod n) + ... an) mod n
```

2. **Multiplication**

```
ab mod n = (a mod n).b mod n

- General case: 
a1.a2...an mod n = ((a1 mod n).a2 mod n ...).an mod n
```

- Proof:

```
r = a mod n => a = kn + r
ab mod n = (bkn + br) mod n
         = br mod n
         = (a mod n).b mod n

- Apply to general case:
a1.a2...an mod n = (a1.a2...a(n-1) mod n).an mod n
                 = ...
                 = ((a1 mod n).a2 mod n).a3 mod n...
```

## Properties

1. **Distributivity:**

```
a(b + c) mod n = (ab mod n + ac mod n) mod n
```

- Proof:

```
a(b + c) = ab + ac
=> a(b + c) mod n = (ab + ac) mod n
                  = (ab mod n + ac mod n) mod n
```

2. **Congruence Idempotence:**

```
x mod n = (x mod n) mod n
```

3. **Associativity:**
4. **Commutativity**

**...Others...**

## Applications

- Prevent overflow when dealing with large number
- ...
