# Introduction

- For unweighted graph, we can use BFS to find the shortest path, which is the path with fewest number of edges.
- For weighted graph, when a path has few edges, it doesn't mean it has lower total weight.
- One algorithm to find shortest path in weighted graph is `Dijkstra's algorithm`.

# Description

- Dijkstra's algorithm focuses on 1 source node, and will find the shortest distance to every other node in the graph from the source.
- Use a min heap to stores nodes, along with the weight of the path used to reach that node from the source (the path used to reach source itself has weight 0).
- Keep track of the minimum distance so far from the source to every other node. If the nodes are numbered from 0 to n - 1, use an array `min_distances` of length n to do that. Initially, all values in the array are `infinity`, (except for the distance to the source, which has value 0).
- At each iteration:
  - Pop the node with minimum weight path from the heap.
  - For each `node`, iterate over the neighbors.
  - Let the current weight path from source to `node` as `current_distance`. For a given `neighbor`, let the weight of the edge `node -> neighbor` as `weight`. Traversing to this neighbor results in a path weight of `distance = current_distance + weight`
  - There are 2 cases:
    - `distance >= min_distances[neighbor]` -> we already found a path with shorter (or equal) distance earlier -> no updates required
    - `distance < min_distances[neighbor]` -> this is the shortest path so far -> update `min_distances[neighbor] = distance` and push `(distance, neighbor)` onto the heap.

# Pseudocode

```python
min_distances = [infinity] * n
min_distances[source] = 0

min_heap = [(0, source)]

while (min_heap is not empty):
    current_distance, node = min_heap.pop()
    if current_distance > min_distances[node]:
        # ignore current path if we already found a better one
        continue

    for neighbor, weight in (edges from node):
        neighbor_distance = current_distance + weight

        # update min distance and add to heap if it creates a shorter path
        if (neighbor_distance < min_distances[neighbor]):
            min_distances[neighbor] = neighbor_distance
            min_heap.push((neighbor_distance, neighbor))
```

# Limitation

- Dijkstra's algorithm should only be used on graph _without_ `negative` weight cycles.

## Example:

```
     3
(0)----->(1)
 ^        | -500
 |        |
 |   2    v   1
 --------(2)----->(3)
```

- Let say we run Dijkstra's algorithm on this graph with 0 as source.
- The first time we reach (2): current_distance = -497
- We then reach (0) with distance = -495, which is less than 0.
  So we visit (0) again.
- Every time we complete the `(0) -> (1) -> (2)` cycle, the path's distance decreases, so the code never stop running.
