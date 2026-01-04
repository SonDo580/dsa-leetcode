"""
https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/

There are n cities numbered from 0 to n-1.
Given the array edges where edges[i] = [from_i, to_i, weight_i] represents
a bidirectional and weighted edge between cities from_i and to_i,
and given the integer 'distanceThreshold'.

Return the city with the smallest number of cities that are reachable through some path
and whose distance is at most 'distanceThreshold'.
If there are multiple such cities, return the city with the greatest number.

Notice that the distance of a path connecting cities i and j
is equal to the sum of the edges' weights along that path.
"""

"""
Idea:
- Find the shortest distance between all (i, j) pairs.
  Use Floyd-Warshall algorithm.
- For each city, find the number reachable cities (d[i][j] < distanceThreshold)
- Return the city with the minimum number of reachable cities.
  Loop forward to get the city with greater number later.
"""

import math


def findTheCity(n: int, edges: list[list[int]], distance_threshold: int) -> int:
    # Find the shortest distance between all (i, j) pairs
    d: list[list[int | float]] = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, weight in edges:
        # note that the edges are bidirectional
        d[u][v] = weight
        d[v][u] = weight
    for k in range(1, n + 1):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k - 1] + d[k - 1][j])

    # Find the number of reachable cities from each city
    reachable: list[int] = [0] * n
    for i in range(n - 1):
        for j in range(i + 1, n):
            if d[i][j] <= distance_threshold:
                reachable[i] += 1
                reachable[j] += 1

    # Find greatest-number city with minimum number of reachable cities
    min_reachable = math.inf
    city_with_min_reachable = -1
    for i in range(n):
        if reachable[i] <= min_reachable:
            min_reachable = reachable[i]
            city_with_min_reachable = i

    return city_with_min_reachable

"""
Complexity:
- Let V = n             (number of vertices)
      E = len(edges)    (number of edges)

1. Time complexity: O(V^3)
- Floyd-Warshall: O(V^3)
- Calculate 'reachable': O(V^2)
- Find city with min_reachable: O(V) 

2. Space complexity: O(V^2)
- 'd': O(V^2)
- 'reachable': O(V)
"""