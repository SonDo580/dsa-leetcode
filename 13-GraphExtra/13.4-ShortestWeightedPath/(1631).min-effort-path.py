"""
https://leetcode.com/problems/path-with-minimum-effort/

You are a hiker preparing for an upcoming hike.
You are given 'heights', a 2D array of size rows x columns,
where heights[row][col] represents the height of cell (row, col).

You are situated in the top-left cell, (0, 0),
and you hope to travel to the bottom-right cell, (rows-1, columns-1).

You can move up, down, left, or right,
and you wish to find a route that requires the minimum effort.

A route's effort is the maximum absolute difference in heights between two consecutive cells of the route.

Return the minimum effort required to travel from the top-left cell to the bottom-right cell.
"""

"""
Idea:
- Cells are nodes in graph.
  Neighbors are top/bottom/left/right nodes (in matrix range).
  Edges are bidirectional and have weight = absolute difference.
- Path weight from source to v extending from u: d[v] = max(d[u], w_uv) 
  (not d[u] + w_uv like standard algorithm)
  -> Effect: path weight stays the same or increases.
  -> Edge weights can be considered non-negative.

=> Use Bellman-Ford or Dijkstra to find minimum-weight paths
   from (0, 0) to other nodes, then return the result for (rows-1, cols-1).
"""


# === Approach 1: Bellman-Ford ===
# (Exceed time limit)

import math


def min_effort_path(heights: list[list[int]]) -> int:
    rows = len(heights)
    cols = len(heights[0])
    n = rows * cols
    src = 0  # <-> (0, 0)
    dest = n - 1  # <-> (rows-1, cols-1)

    # Build list of bidirectional weighted edges
    # - only check right/down direction.
    # - the left/up direction is handled by
    #   right/down direction of left/top node.
    edges: list[tuple[int, int, int]] = []
    directions = [(0, 1), (1, 0)]  # right, down
    for u in range(n):
        row_u, col_u = u // cols, u % cols
        for dy, dx in directions:
            row_v, col_v = row_u + dy, col_u + dx
            if (0 <= row_v < rows) and (0 <= col_v < cols):
                v = row_v * cols + col_v
                weight = abs(heights[row_u][col_u] - heights[row_v][col_v])
                edges.append((u, v, weight))

    d = _bellman_ford(n, src, edges)
    return d[dest]


def _bellman_ford(n: int, source: int, edges: list[tuple[int, int, int]]) -> list[int]:
    """Find min effort from source to each node."""
    # Min effort from source to each node using at most k edges
    d = [math.inf] * n

    # k = 0 -> can only reach source
    d[source] = 0

    # min-effort path contains at most n-1 edges
    # (more edges will only increase path effort)
    for _ in range(n):  # k in [1..n-1]
        for u, v, weight in edges:
            # the edges are bidirectional
            if d[u] != math.inf and max(d[u], weight) < d[v]:
                d[v] = max(d[u], weight)
            if d[v] != math.inf and max(d[v], weight) < d[u]:
                d[u] = max(d[v], weight)

    return d


"""
Complexity:
- Number of nodes: V = rows*cols
  Number of edges: E = O(4*V) = O(V)

1. Time complexity: O(V*E) = O(V^2) = O((rows*cols)^2)
- Build 'edges': O(E)
- Bellman-Ford: O(V*E)
  . Init 'd': O(V)
  . Loop: O(V*E)

2. Space complexity: O(V + E) = O(V) = O(rows*cols)
- 'edges': O(E)
- 'd': O(V)
"""

# === Approach 2: Dijkstra ===

from collections import defaultdict
from heapq import heappush, heappop


def min_effort_path(heights: list[list[int]]) -> int:
    rows = len(heights)
    cols = len(heights[0])
    n = rows * cols
    src = 0  # <-> (0, 0)
    dest = n - 1  # <-> (rows-1, cols-1)

    # Build adjacency list
    adj_list: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    directions = [(0, 1), (1, 0)]  # right, down
    for u in range(n):
        row_u, col_u = u // cols, u % cols
        for dy, dx in directions:
            row_v, col_v = row_u + dy, col_u + dx
            if (0 <= row_v < rows) and (0 <= col_v < cols):
                v = row_v * cols + col_v
                weight = abs(heights[row_u][col_u] - heights[row_v][col_v])
                adj_list[u].append((v, weight))
                adj_list[v].append((u, weight))

    d = _dijkstra(n, src, adj_list)
    return d[dest]


def _dijkstra(
    n: int, src: int, adj_list: defaultdict[int, list[tuple[int, int]]]
) -> list[int | float]:
    """Find min effort from source to each node."""
    d = [math.inf] * n
    min_heap: list[tuple[int, int]] = []
    d[src] = 0
    heappush(min_heap, (0, src))

    while min_heap:
        du, u = heappop(min_heap)
        if du > d[u]:
            continue  # d[u] has finalized

        # - allow du == d[u] since we set d[u] when pushing to heap
        # - there's only 1 item with du = d[u] on the heap,
        #   since we only push to heap if found a path with less effort.

        for v, weight in adj_list[u]:
            if max(d[u], weight) < d[v]:
                d[v] = max(d[u], weight)
                heappush(min_heap, (d[v], v))

    return d


"""
Complexity:
- Number of nodes: V = rows*cols
  Number of edges: E = O(4*V) = O(V)

1. Time complexity: O(V + E + E*log(E)) = = O(rows*cols*log(rows*cols))
- Build adjacency list: O(E)
- Dijkstra: O(V + E*log(E))
  . Init 'd': O(V)
  . heappush/heappop in total: O(E*log(E))
    . heap size = O(E) -> each heappush/heappop takes O(log(E))
    . perform once for each edge.

2. Space complexity: O(V + E) = O(rows*cols)
- adjacency list: O(V + E)
- 'd': O(V)
- heap: O(E)
"""
