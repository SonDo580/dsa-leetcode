"""
https://leetcode.com/problems/network-delay-time/

You are given a network of n nodes, labeled from 1 to n.
You are also given 'times', a list of travel times as directed edges.
Each element in times is of the format [u, v, w],
indicating that it takes w time for a signal to go from u to v.
You are also given an integer k.

We will send a signal from node k.
Return the minimum time it takes for every node to receive the signal.
If it's impossible for all nodes to receive the signal, return -1.
"""

"""
Analysis:
- The graph is given as an array of edges.
  Each edge has an associated non-negative weight.
- The answer to the problem can be found by finding the shortest path
  from k to every other node, then taking the maximum of those values.
- Since the graph only has non-negative weights, and source node is provided,
  we can use Dijkstra's algorithm.

=> Algorithm:
- Build the graph as adjacency list:
- Run Dijkstra's algorithm on the graph, starting from k.
  . The nodes are 1-indexed so we can init distance for n + 1 nodes.
    d[0] will not be used.
- Return the maximum value in d (except).
- If the maximum value is infinity, it indicates that there are nodes
  unreachable from k -> return -1.
"""

from collections import defaultdict
import heapq
import math


def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    graph: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    d = _dijkstra_v1(n + 1, k, graph)
    # d = _dijkstra_v2(n + 1, k, graph)
    answer = max(d[1:])
    return answer if answer < math.inf else -1


def _dijkstra_v1(
    n: int, source: int, graph: dict[int, list[tuple[int, int]]]
) -> list[float | int]:
    d: list[float | int] = [math.inf] * n
    heap: list[tuple[int, int]] = []
    heapq.heappush(heap, (0, source))
    while heap:
        du, u = heapq.heappop(heap)
        if du >= d[u]:
            continue
        d[u] = du
        for v, w_uv in graph[u]:
            if du + w_uv < d[v]:
                heapq.heappush(heap, (du + w_uv, v))
    return d


def _dijkstra_v2(
    n: int, source: int, graph: dict[int, list[tuple[int, int]]]
) -> list[float | int]:
    d: list[float | int] = [math.inf] * n
    finalized: list[bool] = [False] * n
    d[source] = 0
    heap: list[tuple[int, int]] = []
    heapq.heappush(heap, (0, source))
    while heap:
        du, u = heapq.heappop(heap)
        if finalized[u]:
            continue
        finalized[u] = True
        for v, w_uv in graph[u]:
            if not finalized[v] and du + w_uv < d[v]:
                d[v] = du + w_uv
                heapq.heappush(heap, (d[v], v))
    return d

"""
Complexity:
- Let V = n = number of nodes.
      E = len(times) = number of edges.

1. Time complexity: O(V + E*log(V))
- Build 'graph': O(E)
- Dijkstra's algorithm: O(V + E*log(V))
- Find answer: O(V)

2. Space complexity: O(V + E)
- 'graph': O(E)
- Dijkstra's algorithm: O(V + E)
"""