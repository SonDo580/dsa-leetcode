"""
https://leetcode.com/problems/minimum-height-trees/description/

A tree is an undirected graph in which any two vertices are connected by exactly one path.
In other words, any connected graph without simple cycles is a tree.

Given a tree of n nodes labelled from 0 to n - 1,
and an array of n - 1 edges where edges[i] = [ai, bi] indicates that
there is an undirected edge between the two nodes ai and bi in the tree,
you can choose any node of the tree as the root.
When you select a node x as the root, the result tree has height h.
Among all possible rooted trees, those with minimum height (i.e. min(h))
are called minimum height trees (MHTs).

Return a list of all MHTs' root labels.
You can return the answer in any order.

The height of a rooted tree is the number of edges
on the longest downward path between the root and a leaf.
"""

# === Approach 1: DFS/BFS (exceed time limit) ===
"""
Idea:
- Try each node as tree root and get tree height.
- Record the roots with min tree height.

Implementation:
- Build adjacency list.
  Use an array to record tree height rooted at each node.
  Use a variable to track minimum tree height so far.
- Get tree height DFS (post-order traversal):
  . height = 1 + max_height_among_children.
    Base case: leaf has height 0
  . Only explore edges in 1 direction (don't go back to parent).
- Get tree height BFS:
  . Use a variable to track level
  . height = last_level
"""

from collections import defaultdict, deque


def min_height_trees(n: int, edges: list[list[int]]) -> list[int]:
    adj_list: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in edges:
        adj_list[x].append(y)
        adj_list[y].append(x)

    heights: list[int] = []
    min_height: int = float("inf")

    def _get_tree_height_dfs(root: int, parent: int | None) -> int:
        height = 0
        for neighbor in adj_list[root]:
            if neighbor != parent:
                height = max(height, 1 + _get_tree_height_dfs(neighbor, root))
        return height

    def _get_tree_height_bfs(root: int) -> int:
        visited: list[bool] = [False] * n
        height = -1
        queue: deque[int] = deque([root])
        visited[root] = True

        while queue:
            height += 1
            curr_len = len(queue)
            for _ in range(curr_len):  # process all nodes at current level
                node = queue.popleft()
                for neighbor in adj_list[node]:
                    if visited[neighbor]:
                        continue  # neighbor must be parent (tree contains no cycles)
                    queue.append(neighbor)
                    visited[neighbor] = True

        return height

    for i in range(n):
        height = _get_tree_height_dfs(i, None)
        # height = _get_tree_height_bfs(i)

        min_height = min(min_height, height)
        heights.append(height)

    return [i for i in range(n) if heights[i] == min_height]


"""
Complexity:
- Number of nodes: n
  Number of edges: E = len(edges) = n - 1 (tree)
  Tree height: h (degenerate tree -> h = O(n))

1. Time complexity: O(n + E + n^2 + n*E) = O(n^2)
- Build adjacency list: O(E)
- DFS/BFS from each node: O(n + E)
  . For all nodes: O(n*(n + E)) = O(n^2 + n*E)
- Collect roots of minimum height trees: O(n)

2. Space complexity: O(n + E) = O(n)
- adjacency list: O(n + E)
- get tree height: O(h) with DFS OR O(n) with BFS
- 'heights': O(n)
"""
