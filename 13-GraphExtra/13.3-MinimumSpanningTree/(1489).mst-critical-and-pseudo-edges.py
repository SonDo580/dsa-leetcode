"""
https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/

Given a weighted undirected connected graph with n vertices numbered from 0 to n - 1,
and an array 'edges' where edges[i] = [ai, bi, weighti]
represents a bidirectional and weighted edge between nodes ai and bi.

A minimum spanning tree (MST) is a subset of the graph's edges that connects
all vertices without cycles and with the minimum possible total edge weight.

Find all the critical and pseudo-critical edges in the given graph's minimum spanning tree (MST).
An MST edge whose deletion from the graph would cause the MST weight to increase is called a critical edge.
On the other hand, a pseudo-critical edge is that which can appear in some MSTs but not all.

Note that you can return the indices of the edges in any order.
"""

"""
Idea:
- The graph is connected -> it must have a spanning tree.

Step 1: Use Kruskal's algorithm to find 1 MST T. 
        Record the total weight, used and un-used edges.
- Sort edges in increasing order of weights.
  . We need to record edge indices -> combine and sort (weight, index).
- At any step, add the edge with the smallest weight to T,
  if it doesn't create cycle.
- Stop when number of edges in T reaches n - 1.

Step 2: Find critical in all MSTs and pseudo-critical edges in T
- Try replacing each edge of T with a remaining edge
  to find a new spanning tree.
  . If total weight increases, or a spanning tree cannot be built
    (number of edges doesn't reach n - 1)
    -> the replaced edge is a critical edge in all MSTs.
  . If total weight is the same
    -> the replaced edge is a pseudo-critical edge in T.

Step 3: Find pseudo-critical edges in other MSTs
- Unclassified edges: all - critical - T_pseudo_critical
- Try to build a spanning tree including 1 unclassified edge:
  . Add all critical edges first.
    Add the target edge.
    Continue Kruskal's algorithm (keep adding next smallest-weight edge).
  . If the new spanning tree has the same weight as T,
    -> target edge is pseudo-critical.
"""


class UnionFind:
    """Union-Find with path compression and union by rank."""

    def __init__(self, n: int):
        # store the root of the component tree each node is in
        # (can be stale after an union).
        self.ancestor: list[int] = [i for i in range(n)]

        # the height of each subtree
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


def find_critical_and_pseudo_critical_edges(
    n: int, edges: list[list[int]]
) -> list[list[int]]:
    # === Step 1 ===
    # - Find 1 MST (T)

    # Sort edges in increasing weight order. Also save original indices.
    edges_with_indices: list[tuple[tuple[int, int, int], int]] = [
        (edge, i) for i, edge in enumerate(edges)
    ]
    edges_with_indices.sort(key=lambda x: x[0][2])
    sorted_edges: list[tuple[int, int, int]] = [x[0] for x in edges_with_indices]

    uf = UnionFind(n)
    t_total_weight = 0

    # indices in sorted_edges
    used_edge_indices: list[int] = []
    remaining_edge_indices: list[int] = []

    for i, edge in enumerate(sorted_edges):
        x, y, weight = edge
        if not uf.union(x, y):  # will create cycle
            remaining_edge_indices.append(i)
            continue

        used_edge_indices.append(i)
        t_total_weight += weight
        if len(used_edge_indices) == n - 1:
            remaining_edge_indices.extend(range(i + 1, len(sorted_edges)))
            break

    # === Step 2 ===
    # - Find critical edges in all MSTs
    # - Find pseudo-critical edges in T

    # indices in sorted_edges
    critical_edges_indices: list[int] = []
    pseudo_critical_edges_indices: list[int] = []

    # Try excluding each used edge in T
    for i in used_edge_indices:
        uf = UnionFind(n)  # reset
        for j in used_edge_indices:
            if j == i:  # exclude i
                continue
            x, y, _ = sorted_edges[j]
            uf.union(x, y)
        total_weight = t_total_weight - sorted_edges[i][2]
        edge_count = n - 2

        # Replace i with 1 remaining edge
        for j in remaining_edge_indices:
            x, y, weight = sorted_edges[j]
            if not uf.union(x, y):  # will create cycle
                continue
            total_weight += weight
            edge_count += 1
            break

        if edge_count < n - 1 or total_weight > t_total_weight:
            critical_edges_indices.append(i)
        else:
            pseudo_critical_edges_indices.append(i)

    # === Step 3 ===
    # - Find remaining pseudo-critical edges in other MSTs

    # Find non-critical edges:
    # (= all - critical = remaining + T_pseudo_critical)
    # -> merge remaining and T_pseudo_critical in sorted order
    non_critical_edges: list[int] = []  # indices in sorted_edges
    i = j = 0
    while i < len(remaining_edge_indices) and j < len(pseudo_critical_edges_indices):
        if remaining_edge_indices[i] < pseudo_critical_edges_indices[j]:
            non_critical_edges.append(remaining_edge_indices[i])
            i += 1
        elif remaining_edge_indices[i] > pseudo_critical_edges_indices[j]:
            non_critical_edges.append(pseudo_critical_edges_indices[j])
            j += 1
    while i < len(remaining_edge_indices):
        non_critical_edges.append(remaining_edge_indices[i])
        i += 1
    while j < len(pseudo_critical_edges_indices):
        non_critical_edges.append(pseudo_critical_edges_indices[j])
        j += 1

    # Try including each unclassified edge
    for i in remaining_edge_indices:
        uf = UnionFind(n)  # reset
        total_weight = 0
        edge_count = 0

        # Add all critical edges
        for j in critical_edges_indices:
            x, y, weight = sorted_edges[j]
            uf.union(x, y)
            total_weight += weight
        edge_count += len(critical_edges_indices)

        # Try including the unclassified edge
        x, y, weight = sorted_edges[i]
        if not uf.union(x, y):  # will create cycle
            continue
        total_weight += weight
        edge_count += 1

        # Continue with non-critical edges except i
        if edge_count < n - 1:
            for j in non_critical_edges:
                if j == i:  # exclude i
                    continue
                x, y, weight = sorted_edges[j]
                if not uf.union(x, y):  # will create cycle
                    continue
                total_weight += weight
                edge_count += 1
                if edge_count == n - 1:
                    break

        if edge_count == n - 1 and total_weight == t_total_weight:  # found another MST
            pseudo_critical_edges_indices.append(i)

    # === Step 4 ===
    # - Recover the original edge indices

    # i is index in sorted_edges
    get_original_index = lambda i: edges_with_indices[i][1]

    return [
        list(map(get_original_index, critical_edges_indices)),
        list(map(get_original_index, pseudo_critical_edges_indices)),
    ]

"""
Complexity:
- Number of node: n
  Number of edges: E = len(edges)
  . worst case: each node is connected to all other nodes -> E = O(n^2)

1. Time complexity: O(E + E*log(E) + n*E + E^2) = O(n*E + E^2)
- Build 'edges_with_indices': O(E)
- Sort 'edges_with_indices': O(E*log(E))
- Build 'sorted_edges': O(E)
- . uf.init: O(n)
  . uf.union: O(alpha(n)) (practically O(1))
    -> for E edges: O(E)
  -> Build 1 MST: O(n + E)
  -> Build E MSTs: O(E*(n + E)) = O(n*E + E^2)
- Produce 'non_critical_edges': O(E)
- Produce result: O(E)

2. Space complexity: O(n + E)
- 'edges_with_indices': O(E)
- Sort 'edges_with_indices': O(E) (timsort) 
- 'sorted_edges': O(E)
- ..._edge_indices: O(E)
- 'uf': O(n) 
"""