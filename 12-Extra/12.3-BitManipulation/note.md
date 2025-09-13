# Important operations

1. OR (a | b)

- If a = 1 or b = 1, the result is 1. Otherwise the result is 0.

2. AND (a & b)

- If a = b = 1, the result is 1. Otherwise the result is 0.

3. XOR (a ^ b)

- If a = 1 and b = 0, or a = 0 and b = 1, the result is 1. Otherwise the result is 0.

4. Left and right shift (<<, >>)

- Shifts move all the bits over 1 place in the respective direction.
- Left shift <=> multiply by 2
  Right shift <=> floor division by 2

## Examples

x = 15, y = 12 => In binary: x = 1111, y = 1100

```
x | y = 1111 = 15
x & y = 1100 = 12
x ^ y = 0011 = 3
x << 1 = 11110 = 30
x >> 1 = 111 = 7
```

# Bitmask

- When we are concerned with specific bits, we can use a mask to check.
- Note:
  - a flipped bit is a bit with value of 1.
  - to flip a bit is to "reverse" its value: 0 -> 1 or 1 -> 0.

## Examples:

- Let say we are interested in the 2nd bit of a number x.
- We can use the mask 100 (binary). Now any operations between x and mask will only be "applied" on the 2nd bit.
- To produce the mask:

```python
mask = 1
mask << 2
```

- To see if the 2nd bit of x is flipped, use mask & x. Because all other bits in mask are 0, the result will be 0 only if the 2nd bit of x is not flipped.
- To flip the 2nd bit of x, use mask ^ x. Because all other bits in mask are 0, the XOR operations will not change any other bits. If the 2nd bit in x is 1, then 1 ^ 1 = 0. If it is 0, then 0 ^ 1 = 1.

# Bitmasks as hashable indicator of "visited"
- Some problems involve using elements from an array at most once (backtracking, dynamic programming) -> we need an indicator of which elements have been used.
- We could use an array, where arr[i] = 1 indicates that the ith element has been used. But array is not hashable, so it's not a viable solution for DP problems where we need to memoize states.
- We could use a tuple, which is hashable. But modifying the tuples on each state change is expensive (tuples are immutable so we need to create an entirely new tuple).
- A bitmask is the best option. Use an integer `mask` where the ith bit is flipped if the ith element has been used. Use XOR to flip a bit when we use an element. Use AND to check if an element has been used.