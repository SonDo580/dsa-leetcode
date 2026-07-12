"""
https://leetcode.com/problems/all-ancestors-of-a-node-in-a-directed-acyclic-graph/

You are given a positive integer n representing the number of nodes of a Directed Acyclic Graph (DAG).
The nodes are numbered from 0 to n - 1 (inclusive).

You are also given a 2D integer array 'edges', where edges[i] = [fromi, toi]
denotes that there is a unidirectional edge from fromi to toi in the graph.

Return a list answer, where answer[i] is the list of ancestors of the ith node,
sorted in ascending order.

A node u is an ancestor of another node v if u can reach v via a set of edges.
"""

# === Approach 1: DFS/BFS ===
"""
- Build adjacency list from 'edges'.
- Start DFS/BFS from each node,
  add start_node as ancestor for all reachable nodes.
- The graph is acyclic but we still need to track visited nodes
  (for a single pass) to avoid re-traversing nodes.
  . Example: a --> b --> c --> ...
             | --> d --> |
- Loop through nodes in order 0 -> n-1 to start traversal,
  so the ancestor lists are populated in ascending order.
  (don't need to sort afterward).
"""

from collections import defaultdict


def get_ancestors(n: int, edges: list[list[int]]) -> list[list[int]]:
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in edges:
        graph[x].append(y)

    ans: list[list[int]] = [[] for _ in range(n)]

    def _dfs(start_node: int, current_node: int, visited: set[int]) -> None:
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                ans[neighbor].append(start_node)
                visited.add(neighbor)
                _dfs(start_node, neighbor, visited)

    for i in range(n):
        _dfs(start_node=i, current_node=i, visited=set([i]))

    return ans

"""
Complexity:
- Number of nodes: n
  Number of edges: E = len(edges)

1. Time complexity: O(E + n + n*(n + E)) = O(n^2 + n*E)
- Build adjacency list: O(E)
- Init 'ans': O(n)
- DFS from n nodes:
  . Each DFS: O(n + E)

2. Space complexity: O(n + E)
- 'graph' (adjacency list): O(n + E)
- 'visited': O(n)
- DFS recursion stack: O(h) = O(n)
"""
