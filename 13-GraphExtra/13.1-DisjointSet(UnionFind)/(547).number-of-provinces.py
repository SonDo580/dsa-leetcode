"""
https://leetcode.com/problems/number-of-provinces/

There are n cities.
Some of them are connected, while some are not.
If city a is connected directly with city b,
and city b is connected directly with city c,
then city a is connected indirectly with city c.

A province is a group of directly or indirectly connected cities
and no other cities outside of the group.

You are given an n x n matrix 'isConnected' where isConnected[i][j] = 1
if the ith city and the jth city are directly connected,
and isConnected[i][j] = 0 otherwise.

Return the total number of provinces.
"""

"""
Analysis:
- The graph is given as an adjacency matrix ('isConnected').
  . Nodes are cities.
  . Provinces are connected components.
-> Problem: Find number of connected components in the graph.
"""

# === Approach 1: DFS/BFS ===
"""
- Since the graph is static, traversal works fine.
- See 'Graph DFS' section.
"""

# === Approach 2: Union-Find ===
# (The graph is undirected)
"""
- Convert the adjacency matrix to list of edges.
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


def num_provinces(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    uf = UnionFind(n)

    # Convert adjacency matrix to list of (undirected) edges
    edges: list[tuple[int, int]] = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                edges.append((i, j))

    # Add all edges
    for edge in edges:
        uf.union(edge[0], edge[1])

    # Return number of connected components
    return uf.count


"""
Complexity:
- Number of nodes: N = len(is_connected)
  Number of edges: E
  . worst case: every node is connected to every other node -> E = O(N^2)

1. Time complexity: O(N + N^2 + E) = O(N^2)
- UnionFind.init(): O(N)
- Generate 'edges': O(N^2)
- Iterate through E edges:
  . UnionFind.union() for each edge: ~~O(1) on average
  
2. Space complexity: O(N + E)
- 'uf': O(N) for 'ancestor' and 'height' arrays
- 'edges': O(E)
"""
