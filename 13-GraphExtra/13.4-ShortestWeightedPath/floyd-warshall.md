# Description

- Floyd-Warshall algorithm is used to find the shortest distance between all pair of nodes in a directed graph without negative-weight cycles.

# Theorem

- See `Theorem` section in `bellman-ford.md`

# Algorithm

**1. DP**

- Let dp[k][i][j] be the shortest distance from vertex i to vertex j, using only the first k vertices (the set {0, ..., k - 1}) as intermediate points. Note that i, j does not have to be in the set of intermediate points; and the vertices are zero-indexed.
- Range of k: [0, V]
  - At most V vertices (all vertices) are on the shortest path, each encountered once. See `Theorem 2`.
- Base case: k = 0 (only direct edges and self-entries)
  - dp[0][i][i] = 0
  - dp[0][i][j] = w_ij if the edge exists, infinity otherwise
- To find the shortest path from i to j using only the first k vertices, we have 2 choices:
  - Exclude (k - 1)th vertex: the shortest path already found using only the first (k - 1) vertices.
  - Include (k - 1)th vertex: the shortest path from i to k PLUS the shortest path from k to j, both using only the first (k - 1) vertices.
- Formula: dp[k][i][j] = min(dp[k-1][i][j], dp[k-1][i][k-1] + dp[k-1][k-1][j])

- **Pseudocode:**

```python
dp = [[[inf] * V for _ in range(V)] for _ in range(V + 1)]

for i in range(V):
    dp[0][i][i] = 0
for u, v, w_uv in edges:
    dp[0][u][v] = w_uv

# allow the first k vertices as intermediate points
for k in range(1, V + 1): # k = 1 -> k = V
    for i in range(V):
        for j in range(V):
            dp[k][i][j] = min(dp[k-1][i][j], dp[k-1][i][k-1] + dp[k-1][k-1][j])
```

- **Complexity:**

```
Time complexity: O(V^3)
- Init 'dp': O(V^3)
- Handle base case: O(V + E)
- Main loop work: O(V^3)
=> Total: O(V^3 + V + E) = O(V^3) since E = O(V^2)

Space complexity: O(V^3) for 'dp'
```

**2.1. DP - Optimize space**

- dp[k] only depends on dp[k-1], so we can use 2 2D matrices to represent them (don't need a 3D matrix).

- **Pseudocode:**

```python
dp = [[inf] * V for _ in range(V)]

# k = 0
for i in range(V):
    dp[i][i] = 0
for u, v, w_uv in edges:
    dp[u][v] = w_uv

# allow the first k vertices as intermediate points
for k in range(1, V + 1): # k = 1 -> k = V
    next_dp = [[inf] * V for _ in range(V)]
    for i in range(V):
        for j in range(V):
            next_dp[i][j] = min(dp[i][j], dp[i][k-1] + dp[k-1][j])
    dp = next_dp
```

- **Complexity:**

```
Time complexity: O(V^3)
- Init 'dp': O(V^2)
- Handle base case: O(V + E)
- Main loop work: O(V * (V^2 + V^2)) = O(V^3)

Space complexity: O(V^2) for 'dp' and 'next_dp'
```

**2.2. DP - Optimize further**

- Use a single V x V matrix and modify it in-place.
- Let's analyze:

  - Formula: d[i][j] = min(d[i][j], d[i][k-1] + d[k-1][j])
  - Formula to update d[i][k-1]: min(d[i][k-1], d[i][k-1] + d[k-1][k-1]) = d[i][k - 1] since d[k-1][k-1] is always 0.
  - Similar for d[k-1][j].
  - We can see that during the kth iteration _(add the (k - 1)th vertex as an intermediate point)_, d[i][k-1] and d[k-1][j] remains exactly the same as the (k - 1)th iteration.
  - Thus the in-place update is "safe". This behavior is different from Bellman-Ford (2.2), where the in-place update can "look ahead".

- **Pseudocode:**

```python
d = [[inf] * V for _ in range(V)]

# k = 0
for i in range(V):
    d[i][i] = 0
for u, v, w_uv in edges:
    d[u][v] = w_uv

for k in range(1, V + 1): # k = 1 -> k = V
    for i in range(V):
        for j in range(V):
            d[i][j] = min(d[i][j], d[i][k-1] + d[k-1][j])
```

- **Alternative:**

```python
d = [[inf] * V for _ in range(V)]

for i in range(V):
    d[i][i] = 0
for u, v, w_uv in edges:
    d[u][v] = w_uv

for k in range(V): # loop from 0 to V - 1 instead of 1 to V
    for i in range(V):
        for j in range(V):
            # use d[i][k] and d[k][j] instead of d[i][k-1] and d[k-1][j]
            d[i][j] = min(d[i][j], d[i][k] + d[k][j])
```

- **Complexity:**

```
Time complexity: O(V^3)
- Init 'd': O(V^2)
- Handle base case: O(V + E)
- Main loop work: O(V^3)

Space complexity: O(V^2) for 'd'
```

**3. Detect negative-weight cycle**

- In a graph with no negative-weight cycles, the shortest distance from any node i to itself d[i][i] must be 0. If the algorithm finds a path i -> ... -> i with distance < 0, it means there's a negative-weight cycle through i.
- The largest simple cycle has at most V edges and V vertices (no vertices repeated except the start/end). So we can run the check after the main loop, where all V vertices in the graph have been considered as intermediate points.

- **Pseudocode:**

```python
d = [[inf] * V for _ in range(V)]

for i in range(V):
    d[i][i] = 0
for u, v, w_uv in edges:
    d[u][v] = w_uv

for k in range(1, V + 1):
    for i in range(V):
        for j in range(V):
            d[i][j] = min(d[i][j], d[i][k] + d[k][j])

has_negative_cycle = False
for i in range(V):
    if d[i][i] < 0:
        has_negative_cycle = True
        break
```

- **Complexity:** same as (2.2)
