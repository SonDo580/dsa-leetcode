"""
https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

You have a undirected graph of n nodes.
You are given an integer n and an array edges
where edges[i] = [ai, bi] indicates that there is an edge between ai and bi in the graph.
Return the number of connected components in the graph.
"""

"""
Idea:
- Perform DFS/BFS from any node will visit all nodes 
  in the same connected component.
"""

from collections import defaultdict


def count_connected_components(n: int, edges: list[list[int]]) -> int:
    # Build adjacency list to look up node's neighbors quickly
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in edges:
        graph[x].append(y)
        graph[y].append(x)

    seen: set[int] = set()  # track visited nodes

    def _dfs_recur(node: int):
        """Visit all reachable nodes."""
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                _dfs_recur(neighbor)

    def _dfs_iter(node: int):
        """Visit all reachable nodes."""
        stack: list[int] = [node]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)

    count = 0  # number of connected components
    for node in range(n):
        if node not in seen:
            # If a node hasn't been visited, it must belong to a new connected component
            count += 1

            seen.add(node)
            _dfs_recur(node)

    return count


"""
Complexity:
- Number of nodes: n
  Number of edges: E = len(edges)
  . worst case: every node is connected with every other node -> E = n^2
  Max depth: h
  . worst case: h = O(n)

1. Time complexity: O(n + E)
- Build 'graph': O(E)
- DFS: O(n + E)
  . visit each node once, each edge twice.

2. Space complexity: O(n + E)
- 'graph': O(n + E)
- stack:
  . recursive approach: O(h)
  . iterative approach: O(n)
- 'seen': O(n)
"""