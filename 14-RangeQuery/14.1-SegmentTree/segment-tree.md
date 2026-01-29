# Description

- A data structure that allows efficient querying and updating of intervals (segments) of an array.

# Properties

**1. Is a Balanced Full binary tree:**

- **Details:**
  - full: every node has either 0 or 2 children.
  - balanced: for any node, the heights of left and right subtrees differ by no more than 1.
- **Construction:**
  - every range is split into 2 sub ranges until we hit a single element.
  - always split at the mid point -> the left and right subtree are nearly identical in depth -> the tree's height is O(log(n))

**2. Nodes:**

- Leaf nodes represent info of 1 element (range [i..i]).
- Internal nodes represent aggregated info for a range [i..j].
- Root node represent aggregated info of the entire array (range [0..n-1]).

**3. Representation:**

- The segment tree is represented as a **sparse** array with `4*n` slots, where n is the number of elements in the original array _(some slots can be empty)_.
- For a node with index `i`:
  - left child is at `2*i + 1`.
  - right child is at `2*i + 2`.
  - parent is at `(i - 1) // 2`.
- The root is at index 0.
- Note that a node may have 0 children and root node has no parent.

# Proof

**1. For a node with index `i`, left child is at `2*i + 1`, right child is at `2*i + 2`**

```
- The binary tree is full and balanced -> Every level except the last is completely filled.
- Each level d (d = 0 at the root) can hold 2^d nodes.
- Total number of nodes in all levels before d:
  . 2^0 + 2^1 + ... + 2^(d-1) = 2^d - 1
- Pick the kth node on level d (0 <= k < 2^d). Its index in segment tree array is:
  . i = (2^d - 1) + k
- The k nodes to the left of node i on level d has the first 2*k nodes on level d + 1 as children (keep empty children slots) -> The left child of node i is the (2*k)th node on level d + 1:
  . lci = (2^(d + 1) - 1) + 2*k
        = 2 * (2^d + k) - 1
  . i = (2^d - 1) + k
    -> 2^d + k = i + 1
  . substitute: lci = 2 * (i + 1) - 1 = 2*i + 1
- The right child is next to the left child:
  . rci = lci + 1 = 2*i + 2
```

**2. Why do we need an array with `4*n` slots, where n is the number of elements in the original array**

```
- If n is a power of 2 (n = 2^d), the tree is a perfect binary tree (1 -> 2 -> ... -> 2^d nodes at each level). Total number of nodes is:
  . 2^(d + 1) - 1 (sum of geometric series).
    = 2*2^d - 1
    = 2*n - 1
    < 4*n

- If n is a not power of 2 (2^d < n < 2^(d + 1)), we still need 2^(d + 1) slots for the last level. Total number of slots is:
  . 2^(d + 2) - 1
    = 4*2^d - 1
    < 4*n - 1
    < 4*n
```

**Aside:** The binary heap only needs n slots because it represents a complete binary tree.

**3. Related: Sum of geometric series**

- **General case:**

```
Sn = a*r^0 + a*r^1 + ... + a*r^(n-1)
r*Sn = a*r^1 + a*r^2 + ... + a*r^n
-> (1 - r)*Sn = a - a*r^n
-> Sn = a * (1 - r^n) / (1 - r)   if r != 1
```

- **Special cases:**

```
r = 0: Sn = 0
r = 1: Sn = a*n
0 < r < 1 and n -> inf: (converge) Sn = a / (1 - r)
r < 0 and n -> inf: (diverge)
```

# Intro Problem

- Given an array `arr` of size n, perform 2 types of operations:
  - range_query(L, R): find the sum/min/max of elements from L to R.
  - update(i, x): change the value of arr[i] to x.
- For every range_query, iterate from L to R to aggregate result takes O(n). Each update takes O(1).
- With segment tree, both operations take O(log(n)).

## Implementation

See `segment-tree.py`

# Lazy propagation

- A technique to perform range updates quickly.
- Viable if we can calculate the value of an internal node without visiting its children.
  - Example: add `v` to every element in a range of size `k` -> `new_sum = old_sum + k * v`

## Main idea

- Use an extra tree `lazy` with the same structure as `tree` to store pending updates.
- If the range managed by current node is fully contained in range to update, quickly calculate the new value for that, and accumulate pending update to propagate to its children later (don't update children yet).
- When querying a node, propagate the pending update to its children, and reset its lazy state.

## Implementation

See `segment-tree-lazy.py`
