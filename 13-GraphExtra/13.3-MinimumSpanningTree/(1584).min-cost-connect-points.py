"""
https://leetcode.com/problems/min-cost-to-connect-all-points/

You are given an array 'points' representing integer coordinates of some points on a 2D-plane,
where points[i] = [xi, yi].

The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them:
|xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.

Return the minimum cost to make all points connected.
All points are connected if there is exactly one simple path between any two points.
"""

"""
Analysis:
- The points represent nodes in a graph.
  The graph is undirected, weighted, and connected.
  The edge's weight is the manhattan distance between 2 points.
- Since the graph is connected, it must have a spanning tree.
- The minimum cost to make all points connected is
  the total weight of the minimum spanning tree.
"""


# ===== Kruskal's algorithm =====
# ===============================
class UnionFind:
    """Union-Find with path compression and union by rank."""

    def __init__(self, n: int):
        # store the root of the component tree each node is in.
        # can be stale after an union, so let's call it 'ancestor'.
        self.ancestor: list[int] = [i for i in range(n)]

        # the height of each subtree at node.
        self.height: list[int] = [0] * n

    def find(self, x: int) -> int:
        """
        Find the root of the component tree that x is in.
        Record the root for all nodes on the ancestor chain.
        """
        if x == self.ancestor[x]:
            return x  # x is the root
        self.ancestor[x] = self.find(self.ancestor[x])
        return self.ancestor[x]

    def union(self, x: int, y: int) -> bool:
        """
        Merge 2 component trees by setting 1 root as the parent of the other root.
        The resulting tree should have minimum height.
        If x and y are already in the same tree, return False.
        """
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False

        if self.height[root_x] > self.height[root_y]:
            self.ancestor[root_y] = root_x
        elif self.height[root_x] < self.height[root_y]:
            self.ancestor[root_x] = root_y
        else:
            self.ancestor[root_y] = root_x
            self.height[root_x] += 1
        return True


def min_cost_connect_points(points: list[tuple[int, int]]) -> int:
    n = len(points)  # number of nodes

    # Produce list of weighted edges
    edges: list[tuple[int, int, int]] = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            d = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            edges.append((i, j, d))

    # Sort the edges in ascending order of weights
    edges.sort(key=lambda x: x[2])

    # Build the minimum spanning tree T
    # - Keep adding edges until number of edges of T reaches n - 1.
    # - Always pick the edge with smallest weight at any moment,
    #   if it doesn't create cycle in T.
    uf = UnionFind(n)
    total_w = 0
    edges_count = 0
    for x, y, w in edges:
        if not uf.union(x, y):
            continue
        edges_count += 1
        total_w += w
        if edges_count == n - 1:
            break

    return total_w


"""
Complexity:
- Let N = len(points)   (number of nodes)
- Each point is connected to all other points.
  -> number of edges: E = N - 1 + N - 2 + ... + 1 = N * (N - 1) / 2

1. Time complexity: O(E * log(E)) = O(N^2 * log(N))
- Produce 'edges': O(N^2).
- Sort 'edges': O(E*log(E)) = O(N^2 * log(N^2)) = O(N^2 * 2*log(N)) = O(N^2 * log(N))
- Build minimum spanning tree: O(E) = O(N^2)
  . the union takes O(alpha(N)) (practically O(1))
    where alpha is the Inverse Ackermann function.

2. Space complexity: O(N + E) = O(N^2)
- 'edges': O(E) = O(N^2)
- UnionFind: O(N) for 'ancestor' and 'height'
"""
