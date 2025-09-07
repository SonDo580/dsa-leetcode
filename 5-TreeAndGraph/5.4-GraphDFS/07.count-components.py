# You have a graph of n nodes.
# You are given an integer n and an array edges where edges[i] = [ai, bi] indicates that there is an edge between ai and bi in the graph.
# Return the number of connected components in the graph.

# Example 1:
# Input: n = 5, edges = [[0,1],[1,2],[3,4]]
# Output: 2

# Example 2:
# Input: n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
# Output: 1

# Constraints:
# 1 <= n <= 2000
# 1 <= edges.length <= 5000
# edges[i].length == 2
# 0 <= ai <= bi < n
# ai != bi
# There are no repeated edges

# ===== Implementation =====
# - Pick any node and perform a traversal (let choose DFS), record all reachable nodes.
#   All those nodes form a connected component.
# - Find an unreachable node and perform traversal again.
# - Increase the number of connected components for each group.

from collections import defaultdict


def count_connected_components(n: int, edges: list[list[int]]) -> int:
    # Build hashmap to look up node's neighbors quickly
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in edges:
        graph[x].append(y)
        graph[y].append(x)

    # Set to track visited nodes
    seen: set[int] = set()

    def dfs_recur(node: int):
        """Visit all nodes in a connected component"""
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                dfs_recur(neighbor)

    def dfs_iter(node: int):
        """Visit all nodes in a connected component"""
        stack: list[int] = [node]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)

    num_connected_components = 0
    for node in range(n):
        if node not in seen:
            # If a node hasn't been visited, it must belong to a new connected component
            num_connected_components += 1 

            seen.add(node)
            dfs_recur(node)

    return num_connected_components
