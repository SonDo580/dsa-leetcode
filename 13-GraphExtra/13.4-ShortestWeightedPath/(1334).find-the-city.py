"""
https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/

There are n cities numbered from 0 to n-1.
Given the array 'edges' where edges[i] = [from_i, to_i, weight_i] represents
a bidirectional and weighted edge between cities from_i and to_i,
and given the integer 'distanceThreshold'.

Return the city with the smallest number of cities that are reachable through some path
and whose distance is at most 'distanceThreshold'.
If there are multiple such cities, return the city with the greatest number.

Notice that the distance of a path connecting cities i and j
is equal to the sum of the edges' weights along that path.
"""

# === Approach 1: Floyd-Warshall ===
"""
- Find the shortest distance between all (i, j) pairs.
- If d[i][j] < distanceThreshold,
  increase the number of reachable cities for both i and j.
- Return the city with the minimum number of reachable cities.
  Loop forward to get the city with greater number (label) later.
"""

import math


def find_the_city(n: int, edges: list[list[int]], distance_threshold: int) -> int:
    # Find the shortest distance between all pairs of nodes
    d = _floyd_warshall(n, edges)

    # Find the number of reachable cities from each city
    reachable: list[int] = [0] * n
    for i in range(n - 1):
        for j in range(i + 1, n):
            if d[i][j] <= distance_threshold:
                reachable[i] += 1
                reachable[j] += 1

    # Find greatest-label city with minimum number of reachable cities
    min_reachable = math.inf
    city_with_min_reachable = -1
    for i in range(n):
        if reachable[i] <= min_reachable:
            min_reachable = reachable[i]
            city_with_min_reachable = i

    return city_with_min_reachable


def _floyd_warshall(n: int, edges: list[list[int]]) -> list[list[int | float]]:
    """Find the shortest distance between all pairs of nodes"""
    d: list[list[int | float]] = [[math.inf] * n for _ in range(n)]

    for i in range(n):
        d[i][i] = 0
    for u, v, weight in edges:
        # the edges are bidirectional
        d[u][v] = weight
        d[v][u] = weight

    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k - 1] + d[k - 1][j])

    return d


"""
Complexity:
- Let V = n             (number of vertices)
      E = len(edges)    (number of edges)

1. Time complexity: O(V^3)
- Floyd-Warshall: O(V^3)
- Calculate 'reachable': O(V^2)
- Find answer: O(V)

2. Space complexity: O(V^2)
- 'd': O(V^2)
- 'reachable': O(V)
"""

# === Approach 2: Dijkstra ===
"""
- Constraints: 1 <= weight_i <= 10^4
  -> no negative-weight edges
  -> use Dijkstra starting from each node.
"""

from heapq import heappush, heappop
from collections import defaultdict


def find_the_city(n: int, edges: list[list[int]], distance_threshold: int) -> int:
    # Build adjacency list
    adj_list: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, weight in edges:
        # the edges are bidirectional
        adj_list[u].append((v, weight))
        adj_list[v].append((u, weight))

    # Find the shortest distance between all pairs of nodes
    d: list[list[int | float]] = []
    for i in range(n):
        d.append(_dijkstra(n, i, adj_list))

    # Find the number of reachable cities from each city
    reachable: list[int] = [0] * n
    for i in range(n - 1):
        for j in range(i + 1, n):
            if d[i][j] <= distance_threshold:
                reachable[i] += 1
                reachable[j] += 1

    # Find greatest-label city with minimum number of reachable cities
    min_reachable = math.inf
    city_with_min_reachable = -1
    for i in range(n):
        if reachable[i] <= min_reachable:
            min_reachable = reachable[i]
            city_with_min_reachable = i

    return city_with_min_reachable


def _dijkstra(
    n: int, source: int, adj_list: defaultdict[int, list[tuple[int, int]]]
) -> list[int | float]:
    d = [math.inf] * n
    heap: list[tuple[int, int]] = []
    d[source] = 0
    heappush(heap, (0, source))

    while heap:
        du, u = heappop(heap)
        if du > d[u]:
            continue

        for v, weight in adj_list[u]:
            if du + weight < d[v]:
                d[v] = du + weight
                heappush(heap, (d[v], v))

    return d


"""
Complexity:

1. Time complexity: O(V^2 + V*E*log(E))
- Build adjacency list: O(E)
- Perform Dijkstra for all nodes: O(V^2 + V*E*log(E))
  . each Dijkstra: O(V + E*log(E))
- Calculate 'reachable': O(V^2)
- Find answer: O(V)

2. Space complexity: O(V^2 + E)
- adjacency list: O(V + E)
- 'd': O(V^2) (include all return values of Dijkstra)
- Dijkstra's heap: O(E)
- 'reachable': O(V)
"""
