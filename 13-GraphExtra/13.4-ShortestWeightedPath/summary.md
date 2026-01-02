# Introduction

- For unweighted graphs, we can use BFS to find the shortest path, which is the path with fewest number of edges. For weighted graphs, when a path has fewer edges, it doesn't mean it has lower total weight.
- Algorithms for finding shortest path in weight graphs: Floyd-Warshall, Bellman-Ford, Dijkstra.

# Usage

- If the graph has negative-weight cycles, there is no shortest path.
- If the graph has no negative-weight cycles, and need to find the shortest distance between all vertices -> use Floyd-Warshall algorithm.
- If the graph has no negative-weight cycles, and need to find the shortest distance from a source to other vertices -> use Bellman-Ford algorithm.
- If the graph has no negative-weight edges, and need to find the shortest distance from a source to other vertices -> use Dijkstra's algorithm.

# Edge relaxation

- A edge (u, v, w) can be relaxed if the distance to v can be shortened by going through u.

```
if dist[u] + weight(u, v) < dist[v]:
    dist[v] = dist[u] + weight(u, v)
```
