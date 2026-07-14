# Introduction

- For unweighted graphs, we can use BFS to find the shortest path, which is the path with fewest number of edges. For weighted graphs, when a path has fewer edges, it doesn't mean it has lower total weight.
- Algorithms for finding shortest path in weight graphs: Floyd-Warshall, Bellman-Ford, Dijkstra.

# Usage

- If the graph has negative-weight cycles, there is no shortest path
- To **find the shortest distance between all pairs of vertices**:
  - If the graph has no negative-weight **cycles** but has negative-weight **edges** -> use `Floyd-Warshall`.
  - If the graph has no negative-weight **edges** -> run `Dijkstra` V times starting from each vertex _(or still use `Floyd-Warshall`, less effective)_.
- To **find the shortest distance from a source to other vertices**:
  - If the graph has no negative-weight **cycles** but has negative-weight **edges** -> use `Bellman-Ford`.
  - If the graph has no negative-weight **edges** -> use `Dijkstra` _(or still use `Bellman-Ford`, less effective)_

# Edge relaxation

- Apply when distance from source to v can be shortened by going through u.

```
if dist[u] + weight(u, v) < dist[v]:
    dist[v] = dist[u] + weight(u, v)
```
