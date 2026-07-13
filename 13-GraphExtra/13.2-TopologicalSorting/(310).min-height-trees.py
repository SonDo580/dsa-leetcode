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
- Get tree height with DFS (post-order traversal):
  . height = 1 + max_height_among_children.
    Base case: leaf has height 0
  . Only explore edges in 1 direction (don't go back to parent).
- Get tree height with BFS:
  . Use a variable to track level (height)
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
- get tree height: _ O(h) with DFS 
                  |_ O(n) with BFS
- 'heights': O(n)
"""


# === Optimize ===
"""
Hint: How many MHTs can the graph have at most?
- Let the tree diameter be D. 
  (number of edges on longest path between any 2 nodes).
- Let height = number of nodes in subtree
             = number of edges + 1
- For the tree to have minimum height,
  the root should be the center of the diameter
  (2 candidates if D is odd, 1 candidate if D is even).
  The minimum height is then ceil(D / 2).
  
What if we don't choose the center of the diameter:
- If root is on the diameter (except the candidates), 
  1 branch will have height > ceil(D / 2)
- If root is not on the diameter, 
  the subtree with root on the diameter have minimum height ceil(D/2).
  Combine with the edges from subtree root to root, 
  the tree will have height > ceil(D / 2)

How to get to the center of the diameter: (see below)
"""


# === Approach 2.1: DFS (post-order) to find diameter ===
"""
- Use post-order DFS:
  . Pick any node as root to find the diameter.
  . For each subtree: the diameter is maximum among:
    . diameter of children
    . max_child_height + 2nd_max_child_height
      (child_height = number of nodes in subtree
                    = number of edges in subtree + 1)
  . Record the decision at each node to find the diameter later.
- Traverse the decisions backward to collect nodes in the diameter:
  . If the decision is choosing diameter of a child,
    go to that child.
  . If the decision is combining heights of 2 highest children,
    find the longest path from each child to a leaf and
    combine with current node to construct the diameter.
- Find longest path from tree root to a leaf
  (tree height = length of that path):
  Use post-order DFS:
  . node.height = 1 + max(child.height for all children) 
  . base case: leaf: height = 1.
  . Besides the height, return nodes on the longest path 
    (order from leaf to subtree root).
    Append subtree root to the longest path among children.
- After recording all nodes on the diameter,
  return the node(s) at the center. 
"""


def min_height_trees(n: int, edges: list[list[int]]) -> list[int]:
    assert n == len(edges) + 1
    if n == 1:
        return [0]

    adj_list: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in edges:
        adj_list[x].append(y)
        adj_list[y].append(x)

    # convention:
    # - int -> pick diameter of that subtree
    # - tuple -> combine heights of those 2 subtrees
    decisions: list[int | tuple[int, int | None]] = [None] * n

    def _is_leaf(node: int, parent: int | None) -> bool:
        # exclude root
        return len(adj_list[node]) == 1 and adj_list[node][0] == parent

    def _get_diameter_and_height(node: int, parent: int | None) -> tuple[int, int]:
        """Return (diameter, height). Record the decision at node."""
        if _is_leaf(node, parent):
            return 0, 1

        max_child_diameter = -1
        max_child_height = 0
        second_max_child_height = -1
        child_with_max_diameter = None
        child_with_max_height = None
        child_with_second_max_height = None

        for neighbor in adj_list[node]:
            if neighbor == parent:
                continue

            child_diameter, child_height = _get_diameter_and_height(neighbor, node)

            if child_diameter > max_child_diameter:
                max_child_diameter = child_diameter
                child_with_max_diameter = neighbor

            if child_height >= max_child_height:
                # the '=' is required (2 children can have the same max height)
                second_max_child_height = max_child_height
                child_with_second_max_height = child_with_max_height
                max_child_height = child_height
                child_with_max_height = neighbor
            elif child_height > second_max_child_height:
                second_max_child_height = child_height
                child_with_second_max_height = neighbor

        assert child_with_max_diameter is not None
        assert child_with_max_height is not None

        diameter = max(max_child_diameter, max_child_height + second_max_child_height)
        height = 1 + max_child_height

        if diameter == max_child_height + second_max_child_height:
            decisions[node] = (child_with_max_height, child_with_second_max_height)
        else:
            decisions[node] = child_with_max_diameter

        return diameter, height

    root = 0  # arbitrarily pick 1 node as root
    tree_diameter, _ = _get_diameter_and_height(root, None)

    def _get_height_path(node: int | None, parent: int | None) -> list[int]:
        """Find nodes on longest path from subtree root to a leaf."""
        if node is None:
            return []
        if _is_leaf(node, parent):
            return [node]

        max_child_height = 0
        max_child_height_path = None
        for neighbor in adj_list[node]:
            if neighbor == parent:
                continue
            child_height_path = _get_height_path(neighbor, node)
            if len(child_height_path) > max_child_height:
                max_child_height = len(child_height_path)
                max_child_height_path = child_height_path

        assert max_child_height_path is not None
        max_child_height_path.append(node)
        return max_child_height_path

    # Traverse decisions backward until diameter = heights of 2 subtrees
    subtree = root
    decision = decisions[subtree]
    while isinstance(decision, int):
        subtree = decision
        decision = decisions[subtree]
    assert isinstance(decision, tuple)
    left_child, right_child = decision

    left_path = _get_height_path(left_child, subtree)
    right_path = _get_height_path(right_child, subtree)
    diameter_path = left_path + [subtree] + right_path[::-1]
    assert len(diameter_path) == tree_diameter + 1

    mid = len(diameter_path) // 2
    if len(diameter_path) % 2 == 0:  # 2 MHT roots
        return [diameter_path[mid - 1], diameter_path[mid]]
    else:  # 1 MHT root
        return [diameter_path[mid]]


"""
Complexity:
- Number of nodes: n
  Number of edges: E = len(edges) = n - 1 (tree)
  Tree height: h (degenerate tree -> h = O(n))

1. Time complexity: O(n + E) = O(n)
- Build adjacency list: O(E)
- DFS (1) to find tree diameter: O(n + E) 
- Traverse 'decisions': O(n)
- DFS (2) to find 2 parts of diameter path: O(n + E)
- Construct diameter path: O(n)

2. Space complexity: O(n + E + h + h*n) = O(h*n)
- adjacency list: O(n + E)
- 'decisions': O(n)
- DFS (1) recursion stack: O(h)
- DFS (2) recursion stack: O(h*n)
- 'left/right/diameter_path': O(n)
"""
