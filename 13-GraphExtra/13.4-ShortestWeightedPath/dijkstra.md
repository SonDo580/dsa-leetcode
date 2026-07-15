# Description

- Dijkstra's algorithm finds the shortest distance from 1 source to every other node in a graph with **no negative-weight edges**.

# Algorithm

- Use a min heap to store (path_weight, node)s, where `path_weight` is total weight of the path used to reach node from source.
- Keep track of the minimum distance so far from the source to every other node. If the nodes are numbered from 0 to n - 1, use an array `min_distances` of length n. Initially, min_distances[source] = 0, min_distances[other] = `infinity`.
- In each iteration:
  - Pop the node with minimum path weight from the heap.
    Let the path weight be `current_distance`.
  - For a given neighbor, let the weight of the edge (node, neighbor) be `weight`. Traversing to this neighbor results in a path weight of `distance = current_distance + weight`
  - If `distance < min_distances[neighbor]`, update `min_distances[neighbor] = distance`, and push `(distance, neighbor)` onto the heap _(to improve min distances of its neighbors later)_.
- The 1st time a node is popped from the min heap, its shortest distance from source is **finalized**.

## Pseudocode

**1. With `finalized` array**

```python
d = [infinity] * n
finalized = [False] * n
d[source] = 0
min_heap = [(0, source)]

while min_heap:
    du, u = min_heap.pop()

    # there can be multiple items with the same u (different distances) on the heap
    # -> need this check to skip items after u is finalized
    if finalized[u]:
        continue

    # the 1st time u is popped from the heap,
    # its shortest distance is finalized.
    finalized[u] = True

    for v, w in outgoing[u]:
        if not finalized[v] and du + w < d[v]:
            d[v] = du + w
            min_heap.push((d[v], v))
```

**2.1. Optimize space (same complexity):**

- Don't need `finalized` array.
- When popping (du, u) from heap, skip if we've already found a shorter or equivalent path (du >= d[u]).
- When exploring neighbors, only push to heap if it results in a shorter path (du + w_uv < d[v]).
- **Implementation notes**:
  - Update distance after popping from heap, not when pushing.
  - If we set d[u] when pushing to heap, when popping, the check `du >= d[u]` will evaluate to True, which skips neighbors exploring.

```python
d = [infinity] * n
min_heap = [(0, source)]

while min_heap:
    du, u = min_heap.pop()
    if du >= d[u]:
        # ignore current path if already found a shorter or equivalent one
        # (u's shortest distance from source has been finalized)
        continue

    # update shortest distance from source to u (finalized)
    d[u] = u

    for v, w in outgoing[u]:
        # add (path_weight, v) to heap if found a shorter path to v
        if du + w < d[v]:
            min_heap.push((du + w, v))
```

**2.2. Alternative**

- Update shortest distance when pushing to heap, not when popping.
- The check `du >= d[u]` must be changed to `du > d[u]` to allow `du == d[u]` (since d[u] has been set when pushing).

```python
d = [infinity] * n
d[source] = 0 # update when push
min_heap = [(0, source)]

while min_heap:
    du, u = min_heap.pop()
    if du > d[u]:
        # u's shortest distance from source has been finalized
        continue
    # - allow du == d[u] since d[u] is set before pushing to heap
    # - there's only 1 item with du == d[u] on the heap,
    #   since we only push if found a shorter path.

    for v, w in outgoing[u]:
        # add (path_weight, v) to heap if found a shorter path to v
        if du + w < d[v]:
            d[v] = du + w # update when push
            min_heap.push((d[v], v))
```

# Complexity

- Let V = number of vertices, E = number of edges
- The heap is a binary heap.

```
Time complexity: O(V + E*log(E))
- Init 'd': O(V)
- heappush/heappop: O(E*log(E)) in total
  . heap size = O(E) -> push/pop takes O(log(E))
  . perform once for each edge.
- Update d[u]: O(V) in total (perform once for each node)

Space complexity: O(V + E)
- 'd': O(V)
- heap: O(E)
```

# Limitation

- Dijkstra's algorithm can only be used on weighted directed graph with no negative-weight edges.

## Consequence of limitation

- The first time a node is popped from the min heap, its shortest distance from source is **finalized**.

## Examples without limitation

1. Negative weight cycle:

```
 A --------
 ^        | -500
 |        |
 | 2      v
 -------- B
```

- Let's run Dijkstra's algorithm on this graph with A as source.
- (0, A) is popped from the heap and finalized.
  Neighbors: [B]. Record d[B] = -500. Push (-500, B) to the heap.
- (-500, B) is popped from the heap and finalized.
  Neighbors: [A]. A is already finalized, so we don't update d[A].
- The final d[A] is 0, which is incorrect, since we can always decrease it by traversing through the cycle A -> B -> A (-500 + 2 = -498 in each pass).

2. No cycles, but has negative weight edge:

```
     3
 A -----> B
 |        |
 |        | -2
 | 2      v
 -------> C
```

- Let's run Dijkstra's algorithm on this graph with A as source.
- (0, A) is popped from the heap and finalized.
  Neighbors: [B, C].
  Record d[B] = 3. Push (3, B) to the heap.
  Record d[C] = 2. Push (2, C) to the heap.
- (2, C) is popped from the heap and finalized.
- (3, B) is popped from the heap and finalized.
  Neighbors: [C]. C is already finalized, so we don't update d[C].
- The final d[C] is 2 (A -> C). But the correct answer is d[c] = 3 - 2 = 1 (path A -> B -> C).

# Extension: Record concrete paths

## Idea

- Use an array `parent` to track the previous node that reaches current node through the shortest path.
- After Dijkstra's algorithm completes, traverse backward from a node to `source` through `parent` (backtracking).
- There may be multiple shortest paths to reach a node, so each entry of `parent` should be an array.

## Pseudocode

- `Dijkstra`: extend (2.2)

```python
d = [inf] * n
parent = [[] for _ in range(n)]

d[source] = 0
min_heap = [(0, source)]

while min_heap:
    du, u = min_heap.pop()
    if du > u:
        continue

    # - allow du == d[u] since d[u] is set when pushing to heap
    # - there's only 1 (du, u) with du = d[u]
    #   -> the following loop only executes once.
    #   -> will not append duplicate parent (u) for a neighbor v.

    for v, w in outgoing[u]:
        dv = du + w

        # found shorter path
        if dv < d[v]:
            d[v] = dv
            parent[v] = [u] # reset
            min_heap.push((d[v], v))

        # tie path found
        elif dv == d[v]:
            parent[v].append(u)
            # don't append to min_heap
```

- `Backtracking` to find all shortest paths:

```python
def find_all_shortest_path(target: int) -> list[list[int]]:
    target: int = ...
    paths: list[list[int]] = []

    def backtrack(curr_node: int, curr_path: list[int]) -> None:
        if curr_node == source:
            paths.append(curr_path[::-1])
            return

        for p in parent[curr_node]:
            curr_path.append(p)
            backtrack(p, curr_path)
            curr_path.pop()

    backtrack(target, [target])
    return paths
```
