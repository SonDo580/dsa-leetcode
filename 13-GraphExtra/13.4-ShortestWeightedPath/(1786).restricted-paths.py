"""
https://leetcode.com/problems/number-of-restricted-paths-from-first-to-last-node/

There is an undirected weighted connected graph.
You are given a positive integer n which denotes that
the graph has n nodes labeled from 1 to n,
and an array 'edges' where each edges[i] = [ui, vi, weighti] denotes that
there is an edge between nodes ui and vi with weight equal to weighti.

A path from node 'start' to node 'end' is a sequence of nodes [z0, z1, z2, ..., zk]
such that z0 = start and zk = end and there is an edge between zi and z(i+1) where 0 <= i <= k-1.

The distance of a path is the sum of the weights on the edges of the path.
Let distanceToLastNode(x) denote the shortest distance of a path between node n and node x.
A restricted path is a path that also satisfies that
distanceToLastNode(zi) > distanceToLastNode(z(i+1)) where 0 <= i <= k-1.

Return the number of restricted paths from node 1 to node n.
Since that number may be too large, return it modulo 10^9 + 7.
"""

"""
Idea:
- First, we need to find the shortest distance from every node to node n.
  . The graph is undirected so that's also the shortest distance from node n to every node.
  . The graph has no negative-weight edges
    -> Use Dijkstra (or Bellman-Ford).
- After that, perform backtracking to find restricted paths.
  . Start from node 1.
  . At each step, only explore neighbors with smaller distance to n.
  . Record a path when node n is reached
    (the graph is connected so we can always reach n).
- Implementation notes:
  . The nodes are from 1 to n, so perform Dijkstra with N = n + 1.
    d[0] will not be used.
  . Build the graph as adjacency list to find neighbors quickly.
- Optimize backtracking:
  . A sub-path may appear in multiple valid paths.
    -> Use DP to avoid duplicate works.
  . Let dp(u) returns number of restricted path from u to n.
  . Each restricted path from u to n 
    = u prepend to a restricted path from a neighbor v of u to n.
      if distance_to_n[v] < distance_to_n[u]
    -> dp(u) = sum(dp(v) for v in neighbors[u] if d_to_n[v] < d_to_n[u])
  . Base case: u = n -> count = 1
"""

import math
from collections import defaultdict
import heapq
from functools import cache


def count_restricted_paths(n: int, edges: list[list[int]]) -> int:
    # Build adjacency list
    adj: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w_uv in edges:
        adj[u].append((w_uv, v))
        adj[v].append((w_uv, u))

    # Find shortest distance from every node to node n
    # = shortest distance from node n to every node (undirected graph)
    d_to_n = _dijkstra(n + 1, n, adj)  # entry 0 is not used

    # Count restricted paths from 1 to n
    count = _count_restricted_paths(n, d_to_n, adj)
    return count % 1_000_000_007


def _dijkstra(
    n: int, source: int, adj: dict[int, list[tuple[int, int]]]
) -> list[float | int]:
    d: list[int | float] = [math.inf] * n
    min_heap: list[tuple[int, int]] = []

    d[source] = 0
    heapq.heappush(min_heap, (0, source))

    while min_heap:
        du, u = heapq.heappop(min_heap)
        if du > d[u]:
            continue

        # d[u] has finalized,
        # allow du == du[u] to process its neighbors (once)

        for w_uv, v in adj[u]:
            if du + w_uv < d[v]:
                d[v] = du + w_uv
                heapq.heappush(min_heap, (d[v], v))

    return d


def _count_restricted_paths(
    n: int,
    d_to_n: list[float | int],
    adj: dict[int, list[tuple[int, int]]],
) -> int:
    @cache
    def dp(u: int) -> int:
        """Return number of restricted paths from u to n."""
        if u == n:
            return 1

        count = 0
        for _, v in adj[u]:
            if d_to_n[v] < d_to_n[u]:
                count += dp(v)
        return count

    return dp(1)


"""
Complexity:
- Let V = n           (number of vertices)
      E = len(edges)  (number of edges)

1. Time complexity: O(V + E*log(E))
- Build adjacency list: O(E)
- Dijkstra: O(V + E*log(E))
- Count restricted paths: O(V)

2. Space complexity: O(V + E)
- adjacency list: O(V + E)
- Dijkstra: O(V + E) for 'd' and heap
- Recursion stack for DP: O(V)
"""
