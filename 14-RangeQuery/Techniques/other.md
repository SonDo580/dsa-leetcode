# Square root decomposition

- Split original array into approximately sqrt(n) blocks,
  each block contains approximately sqrt(n) elements.
- Each block holds the aggregated result of its elements.
- When update an element, find the affected block and update its result.
- When query a range:
  - For the blocks that are fully contained inside the range,
    use their precomputed results.
  - For the blocks that are NOT fully contained inside the range,
    iterate over elements to compute result.

# Binary indexed tree (Fenwick tree)

TODO

# Sparse table

TODO
