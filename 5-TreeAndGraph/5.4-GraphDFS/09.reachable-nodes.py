# There is an undirected tree with n nodes labeled from 0 to n - 1 and n - 1 edges.
#
# You are given a 2D integer array 'edges' of length n - 1 where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
# You are also given an integer array 'restricted' which represents restricted nodes.
#
# Return the maximum number of nodes you can reach from node 0 without visiting a restricted node.
#
# Note that node 0 will not be a restricted node.

# Example 1:
# Input: n = 7, edges = [[0,1],[1,2],[3,1],[4,0],[0,5],[5,6]], restricted = [4,5]
# Output: 4
# We have that [0,1,2,3] are the only nodes that can be reached from node 0 without visiting a restricted node.

# Example 2:
# Input: n = 7, edges = [[0,1],[0,2],[0,5],[0,4],[3,2],[6,5]], restricted = [4,2,1]
# Output: 3
# We have that [0,5,6] are the only nodes that can be reached from node 0 without visiting a restricted node.

# Constraints:
# 2 <= n <= 10^5
# edges.length == n - 1
# edges[i].length == 2
# 0 <= ai, bi < n
# ai != bi
# edges represents a valid tree.
# 1 <= restricted.length < n
# 1 <= restricted[i] < n
# All the values of restricted are unique.

# ===== Strategy =====
# - Perform a traversal from node 0 (let choose DFS)
# - Stop exploring a path if reach a restrict nodes
# - Count number of reachable nodes.

from collections import defaultdict


def count_reachable_nodes(n: int, edges: list[list[int]], restricted: list[int]) -> int:
    # convert 'restricted' list to a set for faster lookup
    restricted_set = set(restricted)

    # Build hashmap to look up node's neighbors quickly
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in edges:
        graph[x].append(y)
        graph[y].append(x)

    # Set to track visited nodes
    seen: set[int] = set()

    def dfs_recur(node: int):
        """Count non-restricted nodes reachable from node"""
        count = 1
        for neighbor in graph[node]:
            if neighbor not in seen and neighbor not in restricted_set:
                seen.add(neighbor)
                count += dfs_recur(neighbor)
        return count

    def dfs_iter(node: int):
        """Count non-restricted nodes reachable from node"""
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
    return dfs_recur(0)
