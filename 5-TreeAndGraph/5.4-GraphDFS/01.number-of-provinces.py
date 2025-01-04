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
    seen = set()  # track visited nodes
    
    def dfs(node):
        """Function to visit all nodes in a connected component"""
        for neighbor in graph[node]:
            # check if the node has been visited to prevent cycles
            if neighbor not in seen:
                seen.add(neighbor)
                dfs(neighbor)

    def dfs_iterative(start):
        """Same functionality as dfs. Iterative implementation"""
        stack = [start]
        while len(stack) > 0:
            node = stack.pop()

            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)

    # convert the adjacency matrix to an adjacency list
    n = len(is_connected)
    graph = defaultdict(list)

    for i in range(n - 1):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                graph[i].append(j)
                graph[j].append(i)

    count = 0  # track number of connected components

    for i in range(n):
        if i not in seen:
            # if a node hasn't been visited before, it must belong to a new connected component
            count += 1

            # visit all node of the current connected component
            seen.add(i)
            dfs(i)


# ===== Complexity =====
# - n is the number of nodes
# - e is the number of edges
#
# Worst case: every node is connected with every other node -> e = n^2
#
# Time complexity:
# - DFS on graph: O(n + e)
#   + each node is visited once
#   + each edge is visited twice (we had the visited check to prevent cycles)
# - Build the adjacency list: O(n^2)
# => Overall: O(n^2)
#
# Space complexity:
# - Recursion call stack: O(n)
# - Seen set: O(n)
# - The graph (adjacency list): O(e) for storing the edges
# => Overall: O(n + e)
