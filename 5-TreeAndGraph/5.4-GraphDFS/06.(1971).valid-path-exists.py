"""
https://leetcode.com/problems/find-if-path-exists-in-graph/

There is a bi-directional graph with n vertices,
where each vertex is labeled from 0 to n - 1 (inclusive).
The edges in the graph are represented as a 2D integer array 'edges',
where each edges[i] = [ui, vi] denotes a bi-directional edge between vertex ui and vertex vi.
Every vertex pair is connected by at most one edge, and no vertex has an edge to itself.

You want to determine if there is a valid path that exists from vertex 'source' to vertex 'destination'.

Given 'edges' and the integers n, 'source', and 'destination',
return true if there is a valid path from 'source' to 'destination', or false otherwise.
"""

"""
Idea:
- Perform DFS/BFS starting from source
- Return True if we can reach the destination

Note:
- Mark the node as visited when pushing it to the stack.
  If mark as visited when popping, a node may get pushed multiple times,
  result in redundant work (check visited and skip right away).
"""


from collections import defaultdict


def valid_path_exists(
    n: int, edges: list[list[int]], source: int, destination: int
) -> bool:
    # Build adjacency list to look up node's neighbors quickly
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in edges:
        graph[x].append(y)
        graph[y].append(x)

    seen: set[int] = set()  # track visited nodes

    def _dfs_recur(node: int) -> bool:
        """Return True if can reach destination from node."""
        if node == destination:
            return True
        for neighbor in graph[node]:
            if neighbor in seen:
                continue
            seen.add(neighbor)
            if _dfs_recur(neighbor):
                return True
        return False

    def _dfs_iter(node: int) -> bool:
        """Return True if can reach destination from node."""
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
    return _dfs_recur(source)
    # return _dfs_iter(source)


"""
Complexity:
- Number of nodes: n
  Number of edges: E = len(edges)
  . worst case: every node is connected to every other nodes -> E = O(n^2) 
  Max depth: h
  . worst case: h = O(n)
  
1. Time complexity: O(n + E)
- Build 'graph': O(E)
- DFS: O(n + E)
  . visit each node once, each edge twice. 

2. Space complexity: O(n + E)
- 'graph': O(n + E)
  . n nodes (as keys)
  . total items across entries: 2*E
- 'seen': O(n)
- stack:
  . recursion approach: O(h)
  . iterative approach: O(n)
"""
