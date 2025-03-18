# Concepts

1. **Priority queue**

- An abstract data structure that operates like a regular queue, but each element has an associated priority.
- Elements with higher priority are dequeued before those with lower priority, regardless of the order they are added.
- If priorities are equal, the order follow first-in, first-out rule.

2. **Heap**

- A data structure that implements the `priority queue`.
- Support the following operations:
  - Add an element: O(log n)
  - Remove the minimum/maximum element: O(log n)
  - Find the minimum/maximum element: O(1)
- - Min Heap is configured to find/remove the minimum element
  - Max Heap is configured to find/remove the maximum element

# Implementation

(Example with min heap. Logic is the same for max heap)

- A `binary heap` implements a binary tree, but with an array.
- Each element in the array is a node in the tree.
- Constraints:
  - The smallest element is the root, at index 0
  - If A is the parent of B, then A.val <= B.val
  - The tree must be a `complete tree`
- If a node is at index i, its children are at indices `2i + 1` and `2i + 2`.
- An existing array can be converted to a heap in linear time.

# Explanation

1. The tree must be a `complete tree`

- A complete binary tree is the one where all levels, except possibly th last, are fully filled, and the last level is filled from left to right.
- This allows the `heap` to be stored in a contiguous array. No wasted spaces for gaps.
- A complete binary tree with `n` nodes has a height of O(log2 (n)). This guarantee that insertion and removal take O(log n) time.

2. If a node is at index i, its children are at indices `2i + 1` and `2i + 2`

- At level `k`, there are at most `2^k` nodes
- `m` nodes come before node `i` at level `k`
- `n` nodes come before left child of node `i` at level `k + 1`
- `lci` is the index of the left child in the array
- `rci` is the index of the right child in the array

```
m = i - number of nodes up to level (k - 1)
  = i - (2^0 + 2^1 + ... + 2^(k-1))

n = 2m = 2i - (2^1 + ... + 2^(k-1) + 2^k)

lci = number of nodes up to level k + n
    = (2^0 + 2^1 + ... + 2^(k-1) + 2^k)
      + 2i - (2^1 + ... + 2^(k-1) + 2^k)
    = 2i + 1

rci = lci + 1 = 2i + 2
```

# Using built-in heap implementations:

- Some languages implement a min heap by default, while some implement a max heap by default.
- If we're dealing with numbers and want to deal with the opposite type of heap that a language implements, a way to do this is to multiply all numbers by -1
