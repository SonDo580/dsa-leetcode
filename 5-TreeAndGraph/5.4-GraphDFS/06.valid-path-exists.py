# There is a bi-directional graph with n vertices,
# where each vertex is labeled from 0 to n - 1 (inclusive).
# The edges in the graph are represented as a 2D integer array edges,
# where each edges[i] = [ui, vi] denotes a bi-directional edge between vertex ui and vertex vi.
# Every vertex pair is connected by at most one edge, and no vertex has an edge to itself.
#
# You want to determine if there is a valid path that exists from vertex source to vertex destination.
#
# Given edges and the integers n, source, and destination,
# return true if there is a valid path from source to destination, or false otherwise.

# Example 1:
# Input: n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2
# Output: true
# Explanation: There are two paths from vertex 0 to vertex 2:
# - 0 → 1 → 2
# - 0 → 2

# Example 2:
# Input: n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5
# Output: false
# Explanation: There is no path from vertex 0 to vertex 5.

# Constraints:
# 1 <= n <= 2 * 10^5
# 0 <= edges.length <= 2 * 10^5
# edges[i].length == 2
# 0 <= ui, vi <= n - 1
# ui != vi
# 0 <= source, destination <= n - 1
# There are no duplicate edges.
# There are no self edges.


# ===== Strategy =====
# - Perform a DFS starting from source
# - Return true if we can reach the destination


from collections import defaultdict


def valid_path_exists(
    n: int, edges: list[list[int]], source: int, destination: int
) -> bool:
    # Build hashmap to look up node's neighbors quickly
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in edges:
        graph[x].append(y)
        graph[y].append(x)

    # Set to track visited nodes
    seen: set[int] = set()

    def dfs_recur(node: int) -> bool:
        """Return True if can reach destination from node, False otherwise"""
        if node == destination:
            return True

        for neighbor in graph[node]:
            if neighbor in seen:
                continue

            seen.add(neighbor)
            destination_reachable = dfs_recur(neighbor)
            if destination_reachable:
                return True

        return False

    def dfs_iter(node: int) -> bool:
        """Return True if can reach destination from node, False otherwise"""
        stack: list[int] = [node]

        while stack:
            node = stack.pop()

            if node == destination:
                return True

            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)

        return False

    seen.add(source)
    return dfs_iter(source)


# ===== Implementation notes =====
# - In the iterative approach, mark the node as visited before pushing it to the stack.
# - If mark after popping, multiple instances of a node can be added to the stack,
#   result in lots of redundant work.
#
# - Example: perform DFS on the following graph:
#  0---1---|
#  |   |   |
#  2---|   |
#  |       |
#  3-------|
#
# - States of `stack` and `seen` if mark after popping:
# stack = [0]           seen = {}
# stack = [1, 2]        seen = {0}
# stack = [1, 1, 3]     seen = {0, 2}
# stack = [1, 1, 1]     seen = {0, 2, 3}
# stack = [1, 1]        seen = {0, 2, 3, 1}
# stack = [1]           seen = {0, 2, 3, 1}
# stack = []            seen = {0, 2, 3, 1}
#
# - States of `stack` and `seen` if mark before pushing:
# stack = [0]           seen = {0}
# stack = [1, 2]        seen = {0, 1, 2}
# stack = [1, 3]        seen = {0, 1, 2, 3}
# stack = [1]           seen = {0, 1, 2, 3}
# stack = []            seen = {0, 1, 2, 3}
