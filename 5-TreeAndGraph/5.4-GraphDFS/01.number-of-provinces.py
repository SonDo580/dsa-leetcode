# There are n cities. A province is a group of directly or
# indirectly connected cities and no other cities outside of the group.
# You are given an n x n matrix isConnected where
# isConnected[i][j] = isConnected[j][i] = 1 if
# the ith city and the jth city are directly connected,
# and isConnected[i][j] = 0 otherwise.
# Return the total number of provinces.

# ===== Analyze =====
# - This is an undirected graph where the graph is given as an adjacency matrix
# - The problem is asking for the number of connected components
# - Because the graph is undirected, a DFS from any node will visit every node
#   in the connected component it belongs to.
# - To avoid cycles with undirected graph, track visited nodes with a set
#   (OR a boolean array)
#
# Note:
# - a connected component is a maximal set of vertices such that
#   there exists a path between every pair of vertices within the set.

from typing import List
from collections import defaultdict


def count_provinces(is_connected: List[List[int]]) -> int:
    def dfs(node):
        """Function to visit all nodes in a connected component"""
        # mark the current node as visited
        seen.add(node)

        # visit the neighbors
        for neighbor in graph[node]:
            # check if the node has been visited to prevent cycles
            if neighbor not in seen:
                dfs(neighbor)

    def dfs_iterative(start):
        """Same functionality as dfs. Iterative implementation"""
        stack = [start]
        while len(stack) > 0:
            node = stack.pop()
            seen.add(start)

            for neighbor in graph[node]:
                if neighbor not in seen:
                    stack.append(neighbor)

    seen = set()  # track visited nodes
    count = 0  # track number of connected components

    # convert the adjacency matrix to an adjacency list
    n = len(is_connected)
    graph = defaultdict(list)

    for i in range(n - 1):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                graph[i].append(j)
                graph[j].append(i)

    for i in range(n):
        # if a node hasn't been visited before, it must belong to a new connected component
        if i not in seen:
            # increment the number of connected components
            count += 1

            # visit all node of the current connected component
            dfs(i)
