# Description

- Bellman-Ford algorithm is used to find the shortest distance from a source node to every other node in a directed graph without negative-weight cycles.

# Theorem

1. **In a graph with negative-weight cycles, there is no shortest path.**

- If there's a negative-weight cycle, we can keep going along that cycle, reducing the total weight after each pass.

2. **In a graph with no negative-weight cycles with N vertices, the shortest path between any 2 vertices has at most N - 1 edges.**

- Each node on the path from `source` to `destination` should be encountered only once.
- Let's assume that we encounter a node twice. That means we've traversed along a cycle.
  - The graph has no negative-weight cycles.
  - If the cycle has positive weight, the total weight can only increase.
  - If the the cycle has 0 weight, the total weight stays the same, but the path is longer -> **contradict** with what we're trying to find _(the shortest weighted path)_.

# Algorithm

**1.1. DP**

- Let dp[k][i] be the shortest distance from source to vertex i using at most k edges.
- Range of k: [0, V - 1] (see `Theorem 2`).
- Base case:
  - dp[0][source] = 0.
  - dp[0][i] = inf for i != source.

- Recurrence relation:
  - To find the shortest distance to vertex v using at most k edges, look at all vertices u that have an edge (u -> v).
  - Idea: We know the shortest distance to v and each u using at most (k - 1) edges. See if there's a shorter distance to v by going through an u (required 1 additional edge u -> v).
  - Formula: dp[k][v] = min(dp[k - 1][v], min(dp[k - 1][u] + weight(u, v) for u in incoming[v]))

- **Pseudocode:**

```python
dp = [[inf for i in range(V)] for i in range(V)]
dp[0][source] = 0

for k in range(1, V):
    for v in range(V):
        dp[k][v] = dp[k - 1][v]
        for u, w_uv in incoming[v]:
            if dp[k - 1][u] != inf:
                dp[k][v] = min(dp[k][v], dp[k - 1][u] + w_uv)
```

- **Complexity:**

```
Time complexity: O(V^2 + V * E)
- Init 'dp': O(V^2)
- 1st-level loop: O(V) times. For each iteration:
  . Iterate through edges: O(E) across 2nd-level loop iterations

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
- 1st-level loop: O(V) times. For each iteration:
  . 1st 2nd-level loop: O(V)
  . iterate through edges: O(E) across 2nd 2nd-level loop iterations
=> Total: O(V^2 + V * (V + E)) = O(V^2 + V*E)

Space complexity: O(V^2) for 'dp'
```

**1.3. DP (alternative)**

- If the graph is given as a list of weighted edges.
- Idea: We know the shortest distance to u using at most (k - 1) edges. Try to extend that path to find shortest-distance path for v using at most k edges.
- **Note**: we will optimize from this implementation in section 2, 3, 4.

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
- outer loop: O(V) times. For each iteration:
  . 1st inner loop: O(V)
  . 2nd inner loop: O(E)
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

for _ in range(1, V): # k in [1..V-1]
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
- In (2.1), update in kth iteration only use information that is updated in (k - 1)th iteration. In this implementation, we update d[v] based on d[u] in place:
  - If d[u] hasn't been updated in current iteration of k: same as (2.1).
  - If d[u] has been updated in current iteration of k: d[v] may be calculated for path using at most k + 1 edges, not at most k edges.
    But that doesn't violate the goal, it just means we found a shorter path using at most k + 1 to v earlier.
- When the problem has a constraint like **"find the shortest path with exactly/at most k edges"**: must use (2.1).

- **Pseudocode:**

```python
d = [inf] * V
d[source] = 0

for _ in range(1, V):
    for u, v, w in edges:
        if d[u] != inf and d[u] + w < d[v]:
            d[v] = d[u] + w
```

- **Early break**: If we perform a full pass of all edges and no distances change, it means we've already found the shortest paths.

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

- **Detect negative-weight cycle**: After V - 1 iterations, if an edge can still be relaxed, it means there's a negative-weight cycle (see `Theorem 2`) -> Use an extra iteration through edges to detect that.

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

- **Complexity:**

```
Time complexity: O(V * E)
- Init 'd': O(V)
- Outer loop: O(V) times. For each iteration:
  . Loop through edges: O(E)

Space complexity: O(V) for 'd'.
```

**4.1. Find the shortest path with at most K edges**

- Use (2.1), but iterate K times.

**4.2. Find the shortest path with exactly K edges**

- Use (2.1), but iterate K times and without the carry-over.
- In "at most" version, d[v] can stay the same if there're no shorter paths by going through a neighbor u. In "exactly" version, only consider paths extended from the previous iteration by 1 edge.
- In "at most" version, once a node is reached, it stays reached. In "exactly" version, a node might be reachable at k, but unreachable at k + 1, if all neighbors u coming to it are unreachable at k.

```python
# === Example: unreachable nodes ===
"""
(S) -> A -> B
. A is reachable using exactly 1 step
  -> B is reachable using exactly 2 steps
. A is unreachable using exactly 2 steps
  -> B is unreachable using exactly 3 steps
"""
```

- **Pseudocode:**

```python
# d: distance from source to nodes using at most k edges

# k = 0
d = [inf] * V
d[source] = 0

for _ in range(1, K + 1): # k in [1..K]
    # each node must be reached via extending a previous path by 1 edge
    next_d = [inf] * V

    for u, v, w in edges:
        if d[u] != inf and d[u] + w < next_d[v]:
            next_d[v] = d[u] + w
    d = next_d
```

- **Early break**: In iteration k, if all values in `next_d` remain `inf` after the inner loop, all nodes are unreachable using exactly k edges -> all nodes are unreachable using exactly k' edges where k' > k -> stop.

```python
# d: distance from source to nodes using at most k edges

# k = 0
d = [inf] * V
d[source] = 0

for _ in range(1, K + 1): # k in [1..K]
    # each node must be reached via extending a previous path by 1 edge
    next_d = [inf] * V

    changed = False
    for u, v, w in edges:
        if d[u] != inf and d[u] + w < next_d[v]:
            next_d[v] = d[u] + w
            changed = True

    if not changed:
        break
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

# SPFA (Shortest Path Faster Algorithm)

- **Observation**: In standard Bellman-Ford (2.2), we iterate though all edges in every round k. However, an edge (u->v) can only relax d[v] if d[u] was recently update (in round k-1).
- **Improvement**: Only examine edges from nodes whose distances have changed.

- **Implementation**:
  - Main a **queue** to track nodes whose shortest distance estimation has decreased.
  - Avoid re-pushing a node that's already in the queue: use a boolean array `in_queue`.
  - Pop a node u from the queue. Try relaxation through all of its outgoing edges (u, v, w). If d[v] is reduced, push v to the queue (if v isn't already in the queue).
  - Repeat until queue is empty (no more relaxations can occur)
  - Kickstart: add `source` to the queue.

- **Pseudo code**:

```python
# d: shortest path from source to all nodes
d = [inf] * V
d[source] = 0

queue = deque([source])
in_queue = [False] * V
in_queue[source] = True

while queue:
    u = queue.popleft()
    in_queue[u] = False

    for v, w in outgoing[u]:
        if d[u] != inf and d[u] + w < d[v]:
            d[v] = d[u] + w
            if not in_queue[v]:
                queue.append(v)
                in_queue[v] = True
```

- **Complexity**:

```
Time complexity: O(V * E)
(same as Bellman-Ford in worst case, but faster on average)

Space complexity: O(V) for 'd', 'queue', 'in_queue'.
```