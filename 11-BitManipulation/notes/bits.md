# Basic Operations

Perform bitwise:

- `OR (a | b)`: If a = 1 or b = 1, result = 1. Otherwise result = 0.
- `AND (a & b)`: If a = b = 1, result = 1. Otherwise result = 0.
- `XOR (a ^ b)`: If a = b, result = 0. Otherwise result = 1.
- `NOT (~a)`: 0 becomes 1, 1 becomes 0.

# Shifting

- **Left shift (`x << k`)** :
  - shift all bits left by k, discard high bits, fill low bits with 0.
  - <-> multiply by 2^k
- **Logical right shift (`x >>> k`)**:
  - shift all bits right by k, discard low bits, fill high bits with 0.
  - <-> floor division by 2^k for x >= 0 _(rounded down towards 0)_
- **Arithmetic right shift (`x >> k`)**:
  - shift all bits right by k, discard low bits, fill high bits with MSB (keep sign).
  - <-> floor division by 2^k _(rounded down, towards 0 for x >= 0, away from 0 for x < 0)_.

# Properties

- **Idempotent law**:
  - a & a = a
  - a | a = a
- **Commutative law**:
  - a & b = b & a
  - a | b = b | a
  - a ^ b = b ^ a
- **Associativity**:
  - (a & b) & c = a & (b & c)
  - (a | b) | c = (a | b) | c
  - (a ^ b) ^ c = (a ^ b) ^ c
- **Distributive law**:
  - (a & b) | c = (a | c) & (b | c)
  - (a | b) & c = (a & c) | (b & c)
  - (a ^ b) & c = (a & c) ^ (b & c)
- **De Morgan's law**:
  - ~(a & b) = (~a) | (~b)
  - ~(a | b) = (~a) & (~b)
- **Negation**:
  - -a = ~(a - 1) = ~a + 1
  - -1 = ~0
- **AND**:
  - a & 0 = 0
  - a & (-1) = a
  - a & (~a) = 0
- **OR**:
  - a | 0 = a
  - a | (~a) = -1
  - a | (-1) = -1
- **XOR**:
  - a ^ 0 = a
  - a ^ a = 0
  - a ^ (-1) = ~a
- `a & (a - 1)`:
  - Effect: Set the lowest 1 of a to 0.
  - Used in **Brian Kernighan's algorithm** to count number of set bits _(perform repeatedly until a reaches 0)_.
- `a & (-a)`:
  - Equivalent: a & (~(a - 1))
  - Effect: Keep only the lowest 1 of a, set remaining 1's to 0.

# State compression

Example: Track used elements

- Option 1: use array or set
  - not hashable
- Option 2: use tuple
  - hashable but not mutable _(must create new tuple when update state)_
- Option 3: use **bitmask**
  - less space, hashable, fast computation.
  - each bit represents state of an element (1 = used, 0 = unused).
  - update state <-> create new bit mask via bit manipulation.

# Bit manipulation

- **Get kth bit**: (x >> k) & 1
  - Alternative: (x & (1 << k)) > 0 ? 1 : 0
- **Set kth bit to 1**: x | (1 << k)
- **Set kth bit to 0**: x & (~(1 << k))
- **Flip kth bit**: x ^ (1 << k)
