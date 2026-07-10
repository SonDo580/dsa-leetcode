"""
https://leetcode.com/problems/redundant-connection/

In this problem, a tree is an undirected graph that is connected and has no cycles.

You are given a graph that started as a tree with n nodes labeled from 1 to n,
with one additional edge added.
The added edge has two different vertices chosen from 1 to n,
and was not an edge that already existed.
The graph is represented as an array 'edges' of length n where edges[i] = [ai, bi]
indicates that there is an edge between nodes ai and bi in the graph.

Return an edge that can be removed so that the resulting graph is a tree of n nodes.
If there are multiple answers, return the answer that occurs last in the input.
"""

"""
Idea: Use UnionFind
- Iterate through 'edges' and add perform union operation.
  . If adding an edge does not merge 2 connected components,
    that edge is redundant. 
- To record the answer the occur last in the input,
  just iterate forward (normally).
"""


class UnionFind:
    """Implement path compression and union by rank."""

    def __init__(self, n: int):
        self.ancestor = [i for i in range(n)]
        self.height = [0] * n

    def find(self, x: int) -> int:
        """Return root of connected component tree that x is in."""
        if x != self.ancestor[x]:
            self.ancestor[x] = self.find(self.ancestor[x])
        return self.ancestor[x]

    def union(self, x: int, y: int) -> bool:
        """Add edge (x, y). Return True if 2 component trees are merged."""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            # x and y are already in the same component
            return False

        if self.height[root_x] > self.height[root_y]:
            self.ancestor[root_y] = root_x
        elif self.height[root_x] < self.height[root_y]:
            self.ancestor[root_x] = root_y
        else:
            self.ancestor[root_y] = root_x
            self.height[root_x] += 1
        return True


def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    # nodes are labeled from 1 to n
    # -> use n + 1 entries, entry 0 is unused
    n = len(edges)
    uf = UnionFind(n + 1)

    for x, y in edges:
        if not uf.union(x, y):
            return [x, y]
    raise Exception("unreachable")


"""
Complexity:
- Number of edges: E = len(edges) (include the redundant edge)
  Number of nodes: N = (E - 1) + 1 = E (tree graph)

1. Time complexity: O(E)
- Loop through E edges:
  . Perform 'union': O(alpha(n)) ~~ O(1)

2. Space complexity: O(E)
- 'uf': O(N + 1) = O(E)
"""
