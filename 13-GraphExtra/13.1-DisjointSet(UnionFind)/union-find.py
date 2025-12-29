"""
Problem: Check if 2 vertices in a graph are connected.

Approaches:
- If the graph is static, we can perform DFS/BFS from 1 vertex and see
  if we can reach the other vertex (see Graph DFS/BFS section).
  . Time complexity: O(V + E)
    . each node is processed once.
    . adjacent edges of a node is checked once or twice.
  . Space complexity: O(V)
    . BFS: the queue stores all nodes at the current level.
    . DFS: the stack only stores nodes on the current path,
           but worst case is still O(V) for highly skewed graph.
- If edges are added dynamically, DFS/BFS every time is costly.
  We can use the `disjoin set` (`union-find`) data structure.

Main idea:
- Have all (directly or indirectly) connected vertices share the same root node.
  -> Each connected component forms a tree.
- Important functions:
  . find: find the root node of a vertex.
  . union: connect 2 connected components by giving them the same root.
           (perform when adding an edge)
  . connected: 2 vertices are connected if they share the root.
"""

# ===== Basic (Quick Union) =====
# ===============================
"""
- Use a `parent` array to store parent of each node.
- Initial state: all nodes are not connected -> parent[node] = node
- find(x): traverse from x up to root (parent[root] = root)
- union(x, y):
  + normal: make x parent of y (or vice versa).
    . if y is not the root, we have to reverse some edges in y's component.
  + quick union: connect the root of y to the root of x (or vice versa).
    . this reduces the height of the resulting tree,
      and keep all edges intact.
"""


class UnionFind:
    def __init__(self, n: int):
        # vertices: 0 -> n - 1
        self.parent: list[int] = [i for i in range(n)]

    def find(self, x: int) -> int:
        while x != self.parent[x]:
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_y] = root_x  # or vice versa

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


"""
Let n = number of vertices
    h = tree's height

1. Time complexity:
- constructor: O(n) to init `parent` array.
- find: O(h) -> O(n) (worst case: degenerate tree).
- union: O(find).
- connected: O(find).

2. Space complexity: O(n) for `parent` array.
"""


# ===== Quick Find =====
# ======================
"""
- Instead of recording `parent`, record the root of each node.
- find: find root of a node by `root` array.
- union: when root_x becomes parent of root_y, find all nodes with root=root_y
         and update the root of those to root_x.
"""


class UnionFind:
    def __init__(self, n: int):
        self.root: list[int] = [i for i in range(n)]

    def find(self, x: int) -> int:
        return self.root[x]

    def union(self, x: int, y: int) -> None:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return

        self.root[root_y] = root_x  # or vice versa
        for i in range(self.root):
            if self.root[i] == root_y:
                self.root[i] = root_x

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


"""
1. Time complexity:
- constructor: O(n) to init `root` array.
- find: O(1).
- union: O(n) since we have to traverse through `root`.
- connected: O(find).

2. Space complexity: O(n) for `root` array.
"""

# ===== Union by Rank (optimize Quick Union) =====
# ================================================
"""
- In Quick Union implementation, the time complexity of `union` and `find`
  are both O(h), which is O(n) in the worst case (degenerate tree).
- We want to merge 2 trees such that the resulting tree has minimum height.
  . height(x) > height(y) -> parent[y] = x -> resulting height = height(x)
    (if we set parent[x] = y, resulting height is height(x) + 1)
  . height(x) == height(y) -> choose arbitrarily, resulting height = height(x) + 1 
"""


class UnionFind:
    def __init__(self, n: int):
        self.parent: list[int] = [i for i in range(n)]
        self.height: list[int] = [0] * n  # height of each node

    def find(self, x: int) -> int:
        while x != self.parent[x]:
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return

        if self.height[root_x] > self.height[root_y]:
            self.parent[root_y] = root_x
        elif self.height[root_x] < self.height[root_y]:
            self.parent[root_x] = root_y
        else:
            # choose arbitrarily
            self.parent[root_y] = root_x
            self.height[root_x] += 1

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


"""
1. Time complexity:
- constructor: O(n) to init `parent` and `height` arrays.
- find: O(h) -> O(log(n)).
- union: O(find).
- connected: O(find).

2. Space complexity: O(n) for `parent` and `height` arrays.

Extra: Why h -> O(log(n))?
- Let N(h) be the minimum number of nodes required to create a tree of height h.
- Base case: to have h = 0, we need at least N(0) = 1 node
- Recurrence: to reach height h, we need 2 trees that both have height h - 1 
  (if a tree has height < h - 1, the resulting height is still h - 1)
  . N(h) = 2 * N(h - 1)
- Follow the recurrence:
  . N(0) = 1 = 2^0
  . N(1) = 2 * 1 = 2^1
  . N(2) = 2 * 2 = 2^2
  . ...
  . N(h) = 2^h
-> Number of nodes to achieve height h: 
   . n >= N(h) -> n >= 2^h
-> For a fixed number of node:
   . h <= log2(n)
"""

# ===== Path compression (optimize `find`) =======
# ================================================
"""
- Quick Union implementation:
  . From a node, we need to traverse `parent` until we reach the root.
  . If we search root for the same node again (or a node below it in the tree),
    that operation is repeated.
-> Optimize:
   . After the root is found, record the root for all nodes on the path.
   . On subsequent search, we can jump straight to the root.
   . After a merge (parent[root_y] = root_x), searching a node of y tree 
     needs 1 additional jump to reach root_x.
"""


class UnionFind:
    def __init__(self, n: int):
        self.ancestor: list[int] = [i for i in range(n)]

    def find(self, x: int) -> int:
        if x == self.ancestor[x]:
            return x
        self.ancestor[x] = self.find(self.ancestor[x])
        return self.ancestor[x]

    def union(self, x: int, y: int) -> None:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.ancestor[root_y] = root_x  # or vice versa

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


"""
1. Time complexity:
- constructor: O(n) to init `ancestor` array.
- find: 
  + worst case: O(h) -> O(n)
  + best case: O(1) (if the root has been recorded, we can jump to it)
  + average: O(log(n))
- union: O(find).
- connected: O(find).

2. Space complexity: O(n) for `ancestor` array.

Extra:
[Top-Down Analysis of Path Compression]
(https://www.cs.tau.ac.il/~michas/ufind.pdf)
"""


# ===== Path compression + Union by rank =======
# ==============================================


class UnionFind:
    def __init__(self, n: int):
        self.ancestor: list[int] = [i for i in range(n)]
        self.height: list[int] = [0] * n

    def find(self, x: int) -> int:
        if x == self.ancestor[x]:
            return x
        self.ancestor[x] = self.find(self.ancestor[x])
        return self.ancestor[x]

    # without recursion
    def find(self, x: int) -> int:
        # Find root first
        curr = x
        while curr != self.ancestor[curr]:
            curr = self.ancestor[curr]
        root = curr

        # Update root for nodes on the path
        while x != root:
            parent = self.ancestor[x]
            self.ancestor[x] = root
            x = parent

        return root

    def union(self, x: int, y: int) -> None:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return

        if self.height[root_x] > self.height[root_y]:
            self.ancestor[root_y] = root_x
        elif self.height[root_x] < self.height[root_y]:
            self.ancestor[root_x] = root_y
        else:
            self.ancestor[root_y] = root_x
            self.height[root_x] += 1

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


"""
1. Time complexity:
- constructor: O(n) to init `ancestor` and `height` arrays.
- find: O(alpha(n)) on average (~ O(1))
- union: O(find).
- connected: O(find).

2. Space complexity: O(n) for `ancestor` and `height` arrays.

Extra: `alpha` is the Inverse Ackermann function, which grows very slowly.
"""


# ===== Detect cycle =====
# ========================
"""
- UnionFind can be used to detect cycle in undirected graph.
- The graph has cycle if:
  . find(x) and find(y) lead to the same root.
  -> x and y are already in the same tree.
  -> the "obvious" cycle: x -...- root -...- y
                          |__________________|
- Application: 
  . used in Kruskal's algorithm for finding minimum spanning tree.
"""