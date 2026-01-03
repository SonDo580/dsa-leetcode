# Description

- Bellman-Ford algorithm is used to find the shortest distance from a source node to every other node in a directed graph without negative-weight cycles.

# Theorem

1. **In a graph with negative-weight cycles, there is no shortest path.**

- If there's a negative-weight cycle, we can keep going along that cycle, then the total weight will decrease after each pass.

2. **In a graph with no negative-weight cycles with N vertices, the shortest path between any 2 vertices has at most N - 1 edges.**

- Each node on the path from `source` to `destination` should be encountered only once.
- Let's assume that we encounter a node twice. That means we've traversed along a cycle. But the graph has no negative-weight cycles. If the cycle has positive weight, the total weight will increase. If the the cycle hash zero weight, the total weight stays the same, but the path is longer. -> **contradict** with what we're trying to find - the shortest weighted path.

# Algorithm

**1.1. DP**

- Let dp[k][i] be the shortest distance from source to vertex i using at most k edges.
- Range of k: [0, V - 1] (see `Theorem 2`).
- Base case:

  - dp[0][source] = 0.
  - dp[0][i] = inf for other vertices.

- Recurrence relation:

  - To find the shortest distance to vertex v using at most k edges, look at all vertices u that have an edge (u -> v).
  - Idea: We know the shortest distance to v and each u using at most (k - 1) edges. See if there's a shorter distance to v by going through an u (required an additional edge u -> v).
  - Formula: dp[k][v] = min(dp[k - 1][v], min{dp[k - 1][u] + weight(u, v)})

- **Pseudocode:**

```python
dp = [[inf for i in range(V)] for i in range(V)]
dp[0][source] = 0

for k in range(1, V):
    for v in range(V):
        # Case 1: doesn't use kth edge
        dp[k][v] = dp[k - 1][v]

        # Case 2: use kth edge from a neighbor u
        for u, w_uv in incoming[v]:
            if dp[k - 1][u] != inf:
                dp[k][v] = min(dp[k][v], dp[k - 1][u] + w_uv)
```

- **Complexity:**

```
Time complexity: O(V^2 + V * E)
- Init 'dp': O(V^2)
- Outer loop: O(V) times. For each iteration:
  . Iterate through edges: O(E) across inner loop iterations

Space complexity: O(V^2) for 'dp'
```

**1.2. DP (alternative)**

- If the graph is given as adjacency list with outgoing edges.
- Idea: We know the shortest distance to u using at most (k - 1) edges. Try to extend that path to neighbors v to find shortest-distance path for v using at most k edges.

- **Pseudocode:**

```python
dp = [[inf for i in range(V)] for i in range(V)]
dp[0][source] = 0

for k in range(1, V):
    # The shortest path using at most k edges is at least
    # as "good" as the one using at most k - 1 edges
    for v in range(V):
        dp[k][v] = d[k - 1][v]

    for u in range(V):
        if dp[k - 1][u] == inf:
            continue
        for u, w_uv in outgoing[u]:
            dp[k][v] = min(dp[k][v], dp[k - 1][u] + w_uv)
```

- **Complexity:**

```
Time complexity: O(V^2 + V*E)
- Init 'dp': O(V^2)
- Outer loop: O(V) times. For each iteration:
  . first inner loop: O(V)
  . iterate through edges: O(E) across second inner loop iterations

=> Total: O(V^2 + V * (V + E)) = O(V^2 + V*E)

Space complexity: O(V^2) for 'dp'
```

**1.3. DP (alternative)**

- If the graph is given as a list of weighted edges.
- Idea: We know the shortest distance to u using at most (k - 1) edges. Try to extend that path to find shortest-distance path for v using at most k edges.
- Note: we will optimize from this implementation in section 2, 3, 4.

- **Pseudocode:**

```python
dp = [[inf for i in range(V)] for i in range(V)]
dp[0][source] = 0

for k in range(1, V):
    # The shortest path using at most k edges is at least
    # as "good" as the one using at most k - 1 edges
    for v in range(V):
        dp[k][v] = d[k - 1][v]

    for u, v, w_uv in edges:
        if dp[k - 1][u] == inf:
            continue
        dp[k][v] = min(dp[k][v], dp[k - 1][u] + w_uv)
```

- **Complexity:**

```
Time complexity: O(V^2 + V*E)
- Init 'dp': O(V^2)
- Outer loop: O(V) times. For each iteration:
  . first inner loop: O(V)
  . second inner loop: O(E)
=> Total: O(V^2 + V * (V + E)) = O(V^2 + V*E)

Space complexity: O(V^2) for 'dp'
```

**2.1. DP - optimize space**

- Since the recurrence relation is static (dp[k] only depends on dp[k - 1]), we don't need the 2D table. Just use 2 arrays to track the 2 most recent results d[k - 1] and d[k].
- Remember to perform the carry-over (all d[k] entries are initialized to d[k - 1] entries).

- **Pseudocode:**

```python
# d: distance from source to nodes using at most k edges

# k = 0
d = [inf] * V
d[source] = 0

for _ in range(1, V): # k = 1 -> k = V - 1
    next_d = copy(d)
    for u, v, w in edges:
        if d[u] != inf and d[u] + w < next_d[v]:
            next_d[v] = d[u] + w
    d = next_d
```

- **Complexity:**

```
Time complexity: O(V^2 + V * E)
- Init 'd': O(V)
- Outer loop: O(V) times. For each iteration:
  . Copy 'd' to 'next_d': O(V)
  . Loop through edges: O(E)

Space complexity: O(V) for 'd' and 'next_d'.
```

**2.2. DP - optimize further (standard Bellman-Ford)**

- Let's use a single array and update it in-place.
- Carry-over is handled automatically without copying.
- In 2.1, update in kth iteration only use information that is updated in (k - 1)th iteration. In this implementation, we update d[v] based on d[u] in place:
  - If d[u] hasn't been updated in current iteration -> same as 2.1.
  - If d[u] has been updated in current iteration -> d[v] may be calculated for path using at most k + 1 edges, not at most k edges. But that doesn't violate the goal, it just means we found a shorter path earlier.
- When the problem has a constraint like "find the shortest path with exactly/at most k edges", we must use (2.1).

- **Pseudocode:**

```python
d = [inf] * V
d[source] = 0

for _ in range(1, V):
    for u, v, w in edges:
        if d[u] != inf and d[u] + w < d[v]:
            d[v] = d[u] + w
```

- **Complexity:**

```
Time complexity: O(V * E)
- Init 'd': O(V)
- Outer loop: O(V) times. For each iteration:
  . Loop through edges: O(E)

Space complexity: O(V) for 'd'.
```

**3. Early break optimization**

- If we perform a full pass of all edges and no distances change, it means we've already found the shortest paths.
- When the problem has a constraint like "find the shortest path with exactly/at most k edges" -> must use (2.1).

- **Pseudocode:**

```python
d = [inf] * V
d[source] = 0

for _ in range(1, V):
    changed = False
    for u, v, w in edges:
        if d[u] != inf and d[u] + w < d[v]:
            d[v] = d[u] + w
            changed = True

    # if no relaxations happened in this round, we're done
    if not changed:
        break
```

- **Complexity:** same as (2.2)

**4. Detect negative-weight cycle**

- After V - 1 iterations, if an edge can still be relaxed, it means there's a negative-weight cycle (see `Theorem 2`).
- Use an extra iteration through edges to detect that.

- **Pseudocode:**

```python
d = [inf] * V
d[source] = 0

for _ in range(V - 1):
    changed = False
    for u, v, w in edges:
        if d[u] != inf and d[u] + w < d[v]:
            d[v] = d[u] + w
            changed = True
    if not changed:
        break

has_negative_cycle = False
for u, v, w in edges:
    if d[u] != inf and d[u] + w < d[v]:
        has_negative_cycle = True
        break
```

- **Complexity:** same as (2.2)

**5.1. Find the shortest path with at most K edges**

- Use (2.1), but iterate K times.

**5.2. Find the shortest path with at most K edges**

- Use (2.1), but iterate K times and without the carry-over.
- In "at most" algorithm, d[v] can stay the same if there're no shorter paths by going through a neighbor u. In "exactly" algorithm, only consider paths extended from the previous iteration by 1 edge.
- In "at most" version, once a node is reached, it stays reached. In "exactly" version, a node might be reachable at k, but unreachable at k + 1, if all neighbors u coming to it are unreachable at k.

- **Pseudocode:**

```python
# d: distance from source to nodes using at most k edges

# k = 0
d = [inf] * V
d[source] = 0

for _ in range(1, K + 1): # k = 1 -> k = K
    # each node must be reached via extending a previous path by 1 edge
    next_d = [inf] * V

    for u, v, w in edges:
        if d[u] != inf and d[u] + w < next_d[v]:
            next_d[v] = d[u] + w
    d = next_d
```

- **Complexity:**

```
Time complexity: O(K * (V + E))
- Init 'd': O(V)
- Outer loop: O(K) times. For each iteration:
  . Create 'next_d': O(V)
  . Loop through edges: O(E)

Space complexity: O(V) for 'd' and 'next_d'.
```

# Improved Bellman-Ford

TODO
