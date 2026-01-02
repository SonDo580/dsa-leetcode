# Description

- Dijkstra's algorithm focuses on 1 source node, and will find the shortest distance to every other node in the graph from the source.

# Algorithm

- Use a min heap to stores nodes, along with the weight of the path used to reach that node from the source (the path used to reach source itself has weight 0).
- Keep track of the minimum distance so far from the source to every other node. If the nodes are numbered from 0 to n - 1, use an array `min_distances` of length n to do that. Initially, all values in the array are `infinity`, (except for the distance to the source, which has value 0).
- In each iteration:
  - Pop the node with minimum weight path from the heap.
  - For each `node`, iterate over the neighbors.
  - Let the current weight path from source to `node` as `current_distance`. For a given `neighbor`, let the weight of the edge `node -> neighbor` as `weight`. Traversing to this neighbor results in a path weight of `distance = current_distance + weight`
  - There are 2 cases:
    - `distance >= min_distances[neighbor]` -> we already found a path with shorter (or equal) distance earlier -> no updates required
    - `distance < min_distances[neighbor]` -> this is the shortest path so far -> update `min_distances[neighbor] = distance` and push `(distance, neighbor)` onto the heap.

## Pseudocode

1. With `finalized` array

```python
d = [infinity] * n
finalized = [False] * n
d[source] = 0
min_heap = [(0, source)]

while (min_heap is not empty):
    du, u = min_heap.pop()
    if finalized[u]:
        continue

    finalized[u] = True

    for v, w_uv in (edges from u):
        if not finalized[v] and du + w_uv < d[v]:
            d[v] = du + w_uv
            min_heap.push((d[v], neighbor))
```

2. Optimize space (same complexity):

- Don't need to track `finalized` for all nodes.
- When popping (du, u) from heap, skip if we've already found a shorter or equivalent path (skip if du >= d[u]).
- When exploring neighbors, only push to heap if it results in a shorter path (du + w_uv < d[v]).
- Implementation notes: I chose to update distance after popping from heap. This is to handle source node. If we set d[source] = 0 before the `while` loop, the `du >= d[u]` will evaluate to True for the source, thus neighbors exploring is skipped.

```python
d = [infinity] * n
min_heap = [(0, source)]

while (min_heap is not empty):
    du, u = min_heap.pop()
    if du >= d[u]
        # ignore current path if already found a shorter or equivalent one
        continue

    d[u] = u # update distance from source to u

    for v, w_uv in (edges from u):
        # add to heap if it results in a shorter path
        if du + w_uv < d[v]:
            min_heap.push((du + w_uv, v))
```

# Complexity

- Let V = number of vertices, E = number of edges
- The heap is a binary heap.

1. Time complexity: O(V + E \* log(E)) = O(V + E \* log(V))

- Init 'd': O(V)
- heappush/heappop: O(log(E)) per operation, O(E \* log(E)) in total.
- Update d[u]: O(V) in total (once for each node)

2. Space complexity: O(V + E)

- 'd': O(V)
- heap: O(E)

# Limitation

- Dijkstra's algorithm should only be used on weighted directed graph with non-negative weights.

## Consequence of limitation

- The first time a node is popped from the min heap, that's the shortest distance to reach it from source.

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
- After Dijkstra's algorithm completes, traverse backward from a node to `source` through `parent`.
- There may be multiple shortest paths to reach a node (same length), so each entry of `parent` should be an array.

## Example

- shortest paths to reach C from A: (A -> C) and (A -> B -> C)

```
      1
  A -----> B
  |        | 1
  | 2      v
  -------> C
```

## Pseudocode

TODO
