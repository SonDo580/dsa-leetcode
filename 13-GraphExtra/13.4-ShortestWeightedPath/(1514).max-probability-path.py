"""
https://leetcode.com/problems/path-with-maximum-probability/

You are given an undirected weighted graph of n nodes (0-indexed),
represented by an edge list where edges[i] = [a, b] is an undirected edge
connecting the nodes a and b with a probability of success of traversing that edge succProb[i].

Given two nodes 'start' and 'end', find the path with the maximum probability of success
to go from 'start' to 'end' and return its success probability.

If there is no path from 'start' to 'end', return 0.
Your answer will be accepted if it differs from the correct answer by at most 1e-5.
"""

"""
Idea:
- Let edge weight be success probability.
  Path's success probability is compounded by multiplication.
  Since 0 <= probability <= 1, the product decreases or stays the same.
  -> The graph has no negative-weight edges
     (path's success probability is monotonic when going through any edge).
  -> Use (modified) Dijkstra to find path with maximum success probability.
     . Use max heap instead of min heap (with heapq, simulate max heap by negating values).
- Initial state:
  . success probability to reach the source itself is 1.
  . success probability to reach another vertex is 0.
- The first time a node is popped from the heap,
  finalize the maximum success probability to reach it.
"""

from collections import defaultdict
import heapq


def max_probability(
    n: int,
    edges: list[tuple[int, int]],
    succ_prob: list[float],
    start_node: int,
    end_node: int,
) -> float:
    # Build adjacency list
    adj: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for i, edge in enumerate(edges):
        u, v = edge  # bidirectional edge
        adj[u].append((succ_prob[i], v))
        adj[v].append((succ_prob[i], u))

    # Find path with maximum success probability from 'start' to all nodes
    d = _dijkstra(n, start_node, adj)

    return d[end_node]


def _dijkstra(
    n: int, source: int, adj: dict[int, list[tuple[int, int]]]
) -> list[float | int]:
    d: list[int | float] = [0] * n
    max_heap: list[tuple[int, int]] = []
    d[source] = 1
    heapq.heappush(max_heap, (-1, source))

    while max_heap:
        negated_du, u = heapq.heappop(max_heap)
        du = -negated_du
        if du < d[u]:
            continue

        # d[u] has finalized,
        # allow du == du[u] to process its neighbors (once)

        for w_uv, v in adj[u]:
            if du * w_uv > d[v]:
                d[v] = du * w_uv
                heapq.heappush(max_heap, (-d[v], v))

    return d


"""
Complexity:
- Let V = n = number of nodes.
      E = len(times) = number of edges.

1. Time complexity: O(V + E*log(E))
- Build adjacency list: O(E)
- Dijkstra: O(V + E*log(E))

2. Space complexity: O(V + E)
- adjacency list: O(V + E)
- Dijkstra: O(V + E) for 'd' and heap.
"""
