"""
https://leetcode.com/problems/number-of-provinces/

There are n cities. A province is a group of directly or
indirectly connected cities and no other cities outside of the group.
You are given an n x n matrix 'isConnected' where
isConnected[i][j] = isConnected[j][i] = 1 if
the ith city and the jth city are directly connected,
and isConnected[i][j] = 0 otherwise.
Return the total number of provinces.
"""

"""
Analysis:
- This is an undirected graph where the graph is given as an adjacency matrix
- The problem is asking for the number of connected components
  . A connected component is a maximal set of vertices such that
    there exists a path between every pair of vertices within the set.
    
Idea:
- Because the graph is undirected, a DFS/BFS from any node will visit every node
  in the connected component it belongs to.
- To avoid cycles with undirected graph, track visited nodes with a set
  (OR a boolean array).
"""

from collections import defaultdict


def count_provinces(is_connected: list[list[int]]) -> int:
    seen: set[int] = set()  # track visited nodes

    def dfs(node: int) -> None:
        """Visit all nodes reachable from node."""
        for neighbor in graph[node]:
            # check if the node has been visited to prevent cycles
            if neighbor not in seen:
                seen.add(neighbor)
                dfs(neighbor)

    def dfs_iter(start: int) -> None:
        stack: list[int] = [start]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)

    # convert adjacency matrix to adjacency list
    n = len(is_connected)
    graph: defaultdict[int, list[int]] = defaultdict(list)
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

            # visit all nodes in the current connected component
            seen.add(i)
            dfs(i)

    return count


"""
Complexity:
- Number of nodes: n
  Number of edges: E
  . worst case: every node is connected with every other node -> E = n^2
  Max depth: h
  . worst case: h = O(n)

1. Time complexity: O(n + E + n^2) = O(n^2)
- DFS on graph: O(n + E)
  . visit each node once, each edge twice.
- Build adjacency list: O(n^2)

2. Space complexity: O(n + E)
- stack:
  . recursive approach: O(h)
  . iterative approach: O(n)
- 'seen': O(n)
- 'graph' (adjacency list): O(n + E) 
  . n nodes (as keys)
  . total items across entries: 2*E
"""
