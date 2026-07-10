"""
https://leetcode.com/problems/graph-valid-tree/

You have a graph of n nodes labeled from 0 to n - 1.
You are given an integer n and a list of edges where edges[i] = [ai, bi]
indicates that there is an undirected edge between nodes ai and bi in the graph.

Return true if the edges of the given graph make up a valid tree, and false otherwise.
"""

"""
Analysis:
- The graph is a valid tree if it contains no cycles 
  and number of edges is exactly n - 1.

Idea: Use UnionFind
- Quick check: if len(edges) != n-1, return False
- Iterate through 'edges' and perform union operation.
- Detect cycle:
  On union(x, y), find(x) and find(y) lead to the same root.
  -> x and y are already connected on a path through root.
  -> adding direct edge between them forms a cycle.
"""


class UnionFind:
    """Implement path compression and union by rank."""

    def __init__(self, n: int):
        self.ancestor = [i for i in range(n)]
        self.height = [0] * n

    def find(self, x: int) -> int:
        """Return root of connected component tree that x is in."""
        if x == self.ancestor[x]:
            return x
        self.ancestor[x] = self.find(self.ancestor[x])
        return self.ancestor[x]

    def union(self, x: int, y: int) -> bool:
        """Add edge (x, y). Return True if 2 component trees are merged."""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            # x and y are already in the same component (cycle detected)
            return False

        if self.height[root_x] > self.height[root_y]:
            self.ancestor[root_y] = root_x
        elif self.height[root_x] < self.height[root_y]:
            self.ancestor[root_x] = root_y
        else:
            self.ancestor[root_y] = root_x
            self.height[root_x] += 1
        return True


def valid_tree(n: int, edges: list[list[int]]) -> bool:
    if len(edges) != n - 1:
        return False

    uf = UnionFind(n)
    for x, y in edges:
        if not uf.union(x, y):  # cycle detected
            return False
    return True


"""
Complexity: 
- Number of nodes: n
  Number of edges: E = len(edges)

1. Time complexity: O(n + E)
- Init 'uf': O(n)
- Iterate through E edges:
  . Each 'union' takes O(alpha(n)) ~~ O(1)

2. Space complexity: O(n)
- 'uf': O(n)
"""
