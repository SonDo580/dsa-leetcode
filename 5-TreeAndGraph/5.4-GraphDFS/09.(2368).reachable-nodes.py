"""
https://leetcode.com/problems/reachable-nodes-with-restrictions/

There is an undirected tree with n nodes labeled from 0 to n - 1 and n - 1 edges.

You are given a 2D integer array 'edges' of length n - 1 where edges[i] = [ai, bi]
indicates that there is an edge between nodes ai and bi in the tree.
You are also given an integer array 'restricted' which represents restricted nodes.

Return the maximum number of nodes you can reach from node 0 without visiting a restricted node.

Note that node 0 will not be a restricted node.
"""

"""
Idea:
- Perform DFS/BFS from node 0.
- Stop exploring a path if encounter a restrict nodes.
- Count number of reachable nodes.
"""

from collections import defaultdict


def count_reachable_nodes(n: int, edges: list[list[int]], restricted: list[int]) -> int:
    # Convert 'restricted' list to a set for faster lookup
    restricted_set = set(restricted)

    # Build adjacency list to look up node's neighbors quickly
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in edges:
        graph[x].append(y)
        graph[y].append(x)

    seen: set[int] = set()  # track visited nodes

    def _dfs_recur(node: int) -> int:
        """Count non-restricted nodes reachable from node."""
        count = 1
        for neighbor in graph[node]:
            if neighbor not in seen and neighbor not in restricted_set:
                seen.add(neighbor)
                count += _dfs_recur(neighbor)
        return count

    def _dfs_iter(node: int) -> int:
        """Count non-restricted nodes reachable from node."""
        stack: list[int] = [node]
        count = 0
        while stack:
            node = stack.pop()
            count += 1
            for neighbor in graph[node]:
                if neighbor not in seen and neighbor not in restricted_set:
                    seen.add(neighbor)
                    stack.append(neighbor)
        return count

    seen.add(0)
    return _dfs_recur(0)


"""
Complexity:
- Number of nodes: n
  Number of restricted nodes: rn < n -> O(n)
  Number of edges: E = len(edges)
  . worst case: every node is connected with every other node -> E = n^2
  Max depth: h
  . worst case: h = O(n)

1. Time complexity: O(n + E)
- Convert 'restricted' to set: O(n)
- Build 'graph': O(E)
- DFS: O(n + E)
  . visit each node once, each edge twice.

2. Space complexity: O(n + E)
- 'graph': O(n + E)
- 'seen': O(n)
- 'restricted_set': O(n)
- stack:
  . recursive approach: O(h)
  . iterative approach: O(n)
"""
