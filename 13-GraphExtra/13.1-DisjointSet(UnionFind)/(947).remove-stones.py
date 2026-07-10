"""
https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/

On a 2D plane, we place n stones at some integer coordinate points.
Each coordinate point may have at most one stone.

A stone can be removed if it shares either the same row or the same column
as another stone that has not been removed.

Given an array `stones` of length n where stones[i] = [xi, yi]
represents the location of the ith stone,
return the largest possible number of stones that can be removed.
"""

"""
Analysis:
- The locations of the stones form a graph:
  . each location is a node.
  . 2 nodes are connected if their x or y coordinates are equal.
  . the edges are bidirectional.
- We need to find the number of connected components.
  Remove stones until each component has only 1 stone remain.
  -> largest number of stone that can be removed: n - num_connected_components
"""

# ===== Approach 1: DFS/BFS =====
# ===============================
"""
- Build the graph as an adjacency list.
  For each node, check all other nodes for connectivity
  and build a bidirectional edge.
- Perform DFS/BFS from each node
- Start a new connected component if a node hasn't been visited 
  in the previous traversal.
"""

from collections import defaultdict


def remove_stones(stones: list[tuple[int, int]]) -> int:
    n = len(stones)
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for i in range(n - 1):
        for j in range(i + 1, n):
            # xi = xj or yi = yj
            if stones[i][0] == stones[j][0] or stones[i][1] == stones[j][1]:
                graph[i].append(j)
                graph[j].append(i)

    count: int = 0
    seen: set[int] = set()
    stack: list[int] = []

    for i in range(n):
        if i in seen:
            continue

        count += 1
        stack.append(i)
        seen.add(i)

        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor in seen:
                    continue
                stack.append(neighbor)
                seen.add(neighbor)

    return n - count


"""
Complexity:
- Let N = len(stones) = number of nodes
      E = number of edges
      . worst case: each node is connected to every other node
                    (all stones are on the same line)
    -> E = (N - 1) + (N - 2) + ... + 2 + 1 = N * (N - 1) / 2 = O(N^2)

1. Time complexity: O(N^2 + N + E) = O(N^2)
- Build `graph`: O(N^2)
- Graph traversal: O(N + E)
  . each node is processed once, each edge is checked twice.
  
2. Space complexity: O(N + E)
- `graph`: O(E)
- `seen`: O(N)
- stack: O(N)
  . Worst case: 
    . Iterative approach: when all nodes are connected to each other.
      -> we start from 1 node, then add all N - 1 neighbors to the stack.
    . Recursive approach: when the graph degenerates to a linked-list.
      -> max recursion depth is N.
"""


# ===== Approach 2: Union-Find =====
# ==================================
"""
- Iterate through edges and perform `union`.
  At the end, count the number of roots.
- Optimize: Track number of connected components
  . Initially count = n (n nodes, 0 edges).
  . Decrement `count` for every successful `union`.
"""


class UnionFind:
    def __init__(self, n: int):
        self.ancestor = [i for i in range(n)]
        self.height = [0] * n
        self.count = n  # number of connected components

    def find(self, x: int) -> int:
        if x == self.ancestor[x]:
            return x
        self.ancestor[x] = self.find(self.ancestor[x])
        return self.ancestor[x]

    def union(self, x: int, y: int):
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
        self.count -= 1


def remove_stones(stones: list[tuple[int, int]]) -> int:
    n = len(stones)
    uf = UnionFind(n)
    for i in range(n - 1):
        for j in range(n):
            if stones[i][0] == stones[j][0] or stones[i][1] == stones[j][1]:
                uf.union(i, j)
    return n - uf.count


"""
Complexity:

1. Time complexity: O(N^2)
- Number of iterations: O(N^2)
- `union`: O(alpha(n)) ~~ O(1)

2. Space complexity: O(N) for 'uf'
"""
