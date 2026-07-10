"""
https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

You have a graph of n nodes.
You are given an integer n and an array edges where edges[i] = [ai, bi]
indicates that there is an edge between ai and bi in the graph.

Return the number of connected components in the graph.
"""

# === Approach 1: DFS/BFS ===
"""
- Since the graph is static, traversal works fine.
- See 'Graph DFS' section.
"""

# === Approach 2: Union-Find ===
# (The graph is undirected)
"""
- Initially, there are n connected components (n nodes, 0 edges).
- Add 1 edge (x, y) to the graph at a time and perform union operation:
  . If tree containing x and tree containing y are merged,
    decrease the number of connected components.
- Return remaining number of connected components after all edges are added. 
"""


class UnionFind:
    """Implement path compression and union by rank."""

    def __init__(self, n: int):
        # Initially:
        # - each node is root of a component tree containing only itself
        # - all trees have height = 0
        self.ancestor = [i for i in range(n)]
        self.height = [0] * n
        self.count = n  # number of connected components

    def find(self, x: int) -> int:
        """Find root of connected component tree that x is in."""
        return self.__find_recur(x)
        # return self.__find_iter(x)

    def __find_recur(self, x: int) -> int:
        if self.ancestor[x] == x:
            return x

        # record root for all ancestors of x
        # when the recursion stack unwinds
        self.ancestor[x] = self.find(self.ancestor[x])

        return self.ancestor[x]

    def __find_iter(self, x: int) -> int:
        if self.ancestor[x] == x:
            return x

        # Find root
        curr = x
        while curr != self.ancestor[curr]:
            curr = self.ancestor[curr]
        root = curr

        # Record root for nodes on ancestor chain
        curr = x
        while curr != root:
            parent = self.ancestor[curr]
            self.ancestor[curr] = root
            curr = parent

        return root

    def union(self, x: int, y: int) -> None:
        """Add edge (x,y). May connect 2 connected component trees."""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            # x and y are already in the same connected component
            return

        # Connect connected 2 component trees
        self.count -= 1

        # - Should minimize result tree height to keep find() efficient
        #   -> Shorter tree becomes child of taller tree
        if self.height[root_x] > self.height[root_y]:
            self.ancestor[root_y] = root_x
        elif self.height[root_x] < self.height[root_y]:
            self.ancestor[root_x] = root_y

        # - If 2 trees have the same height h, arbitrarily pick one as root
        #   -> Result tree height: h + 1
        else:
            self.ancestor[root_y] = root_x
            self.height[root_x] += 1


def count_components(n: int, edges: list[list[int]]) -> int:
    uf = UnionFind(n)
    for x, y in edges:
        uf.union(x, y)
    return uf.count


"""
Complexity:
- Number of nodes: n
  Number of edges: E = len(edges)
  . worst case: every node is connected to every other node -> E = O(n^2)

1. Time complexity: O(n + E)
- UnionFind.init(): O(n)
- Iterate through E edges:
  . UnionFind.union() for each edge: ~~O(1) on average
  
2. Space complexity: O(n)
- 'uf': O(n) for 'ancestor' and 'height' arrays
"""
