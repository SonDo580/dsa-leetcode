"""
https://leetcode.com/problems/cheapest-flights-within-k-stops/

There are n cities connected by some number of flights.
You are given an array 'flights' where flights[i] = [fromi, toi, pricei]
indicates that there is a flight from city fromi to city toi with cost pricei.

You are also given three integers src, dst, and k,
return the cheapest price from src to dst with at most k stops.
If there is no such route, return -1.
"""

"""
Idea:
- Stops are nodes in a graph.
  Weighted directed edges are given by 'flights'.
  . All prices > 0 (constraint) -> no negative-weight cycles. 
- The cheapest price from src to dst with at most K stops 
  <-> Minimum path weight from src to dst using at most K+1 edges.
=> Use Bellman-Ford
"""

import math


def find_cheapest_price(
    n: int, flights: list[list[int]], src: int, dst: int, k: int
) -> int:
    d = _bellman_ford(n, src, k + 1, flights)
    return d[dst] if d[dst] < math.inf else -1


def _bellman_ford(
    n: int, source: int, k: int, edges: list[tuple[int, int, int]]
) -> list[int | float]:
    """Find distance from source to other nodes using at most k edges."""
    # distance from source to each node using at most k' edges
    d: list[int | float] = [math.inf] * n

    # k' = 0 -> can only reach source itself
    d[source] = 0

    for _ in range(1, k + 1):  # k' in range [1..k]
        next_d = [x for x in d]
        for u, v, weight in edges:
            if d[u] != math.inf and d[u] + weight < next_d[v]:
                next_d[v] = d[u] + weight
        d = next_d

    return d


"""
Complexity:
- Number of nodes: V = n
  Number of edges: E = len(flights) = O(V^2)

1. Time complexity: O(V + k*E) for Bellman-Ford
2. Space complexity: O(V) for 'd'
"""
