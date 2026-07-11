"""
https://leetcode.com/problems/smallest-string-with-swaps/

You are given a string s,
and an array of pairs of indices in the string 'pairs'
where pairs[i] = [a, b] indicates 2 indices(0-indexed) of the string.

You can swap the characters at any pair of indices
in the given pairs any number of times.

Return the lexicographically smallest string that
s can be changed to after using the swaps.
"""

"""
Analysis:
- In the lexicographically smallest string, for each pair, 
  the lexicographically smaller character should come first.
- Treat each index in 'pairs' as a node in graph.
  Then each pairs[i] is an undirected edge.
  -> Within each connected component, sort the nodes by 
     corresponding characters in lexicographically increasing order.
"""

# === Approach 1: DFS/BFS ===
"""
- Build adjacency list:
  . Iterate through pairs and add bidirectional edges.
- Start DFS/BFS from each node:
  . If the node hasn't been visited in previous traversals,
    start a new connected components.
    . Track visited nodes across traversals by 'visited' set.
  . Collect all reachable nodes (index + character) in each pass.
- Build result string:
  . Use a character array of length len(s)
  . If i is not in 'visited': arr[i] = s[i].
    Otherwise: (see next note)
- Process collected nodes for each connected component:
  . Sort index in increasing order.
  . Sort characters in lexicographically increasing order.
  . Record character to put at each index.
"""

from collections import defaultdict


def smallest_string_with_swaps(s: str, pairs: list[list[int]]) -> str:
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in pairs:
        graph[x].append(y)
        graph[y].append(x)

    visited: set[int] = set()  # track visited node across traversals

    def _dfs(start: int) -> tuple[list[int], list[str]]:
        """Return all reachable nodes (index in s + corresponding character)."""
        stack: list[int] = [start]
        visited.add(start)
        indices: list[int] = []
        chars: list[str] = []

        while stack:
            node = stack.pop()
            indices.append(node)
            chars.append(s[node])

            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
                    visited.add(neighbor)

        return indices, chars

    n = len(s)
    result: list[str] = [None] * n  # to construct result string

    for node in graph:
        if node not in visited:
            # Start a new connected component
            indices, chars = _dfs(node)

            indices.sort()
            chars.sort()
            # Put characters in lexicographically increasing order
            # at indices of the connected component
            for i in range(len(indices)):
                result[indices[i]] = chars[i]

    # Fill non-swappable characters
    for i in range(n):
        if i not in visited:
            result[i] = s[i]

    return "".join(result)


"""
Complexity:
- Let n = len(s)
- Number of nodes: N = O(n)
  Number of edges: E = len(pairs)
  . worst case: E = O(n^2) (every node is connected to every other node)

1. Time complexity: O(n + E + n*log(n)) = O(n*log(n) + E)
- Build 'graph': O(E)
- Init 'result': O(n)
- DFS (total): O(n + E)
- Sort 'indices' and 'chars': O(n*log(n))
  (worst case: all nodes are in the same connected component)
- Fill result characters array: O(n)
- Produce result string: O(n)

2. Space complexity: O(n + E)
- 'graph': O(n + E)
- 'visited': O(n)
- DFS stack: O(n)
- 'indices', 'chars': O(n)
- Sorting: O(n) (timsort)
- 'result': O(n)
"""

# === Approach 2: UnionFind ===
"""
- Iterate through edges ('pairs') and perform union operation
- Group nodes in the same connected component:
  . Iterate through uf.ancestor.
  . Perform find(x) for each node (fix if root is stale after union).
  . Group (node + character)s with the same root.
- Build result string and process each connected component:
  . Same as approach 1.
"""


class UnionFind:
    """Implement path compression and union by rank."""

    def __init__(self):
        # root of connected component tree each node is in
        # . can be stale after union() -> fix when find()
        self.ancestor: dict[int, int] = {}

        # subtree height
        self.height: dict[int, int] = {}

    def find(self, x: int) -> int:
        """Return root of connected component tree that x is in."""
        if x != self.ancestor[x]:
            # update root for all ancestors on the chain
            # when recursion stack unwinds
            self.ancestor[x] = self.find(self.ancestor[x])
        return self.ancestor[x]

    def union(self, x: int, y: int) -> None:
        """Add edge (x, y). May merge 2 component trees."""
        for node in [x, y]:
            if node not in self.ancestor:
                self.ancestor[node] = node
                self.height[node] = 0

        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return

        # union by rank: minimize merged tree height
        if self.height[root_x] > self.height[root_y]:
            self.ancestor[root_y] = root_x
        elif self.height[root_x] < self.height[root_y]:
            self.ancestor[root_x] = root_y
        else:
            self.ancestor[root_y] = root_x
            self.height[root_x] += 1


def smallest_string_with_swaps(s: str, pairs: list[list[int]]) -> str:
    uf = UnionFind()
    for x, y in pairs:
        uf.union(x, y)

    # map component tree root -> list of indices & list of characters
    components: dict[int, tuple[list[int], list[str]]] = {}
    for node in uf.ancestor:
        root = uf.find(node)  # fix possibly stale root
        if root not in components:
            components[root] = ([], [])
        components[root][0].append(node)  # index in s
        components[root][1].append(s[node])  # character

    # characters of result string
    # - keep characters intact at non-swappable indices
    result = list(s)

    # Sort each entry and build result
    for indices, chars in components.values():
        indices.sort()
        chars.sort()

        # Put characters in lexicographically increasing order
        # at indices of the connected component
        for i in range(len(indices)):
            result[indices[i]] = chars[i]

    return "".join(result)


"""
Complexity:
- Let n = len(s)
- Number of nodes: N = O(n)
  Number of edges: E = len(pairs)
  . worst case: E = O(n^2) (every node is connected to every other node)

1. Time complexity: O(E + N + n + n*log(n)) = O(n*log(n) + E)
- Iterate through E edges:
  . each union(): ~~O(1)
- Iterate through N nodes in uf.ancestor:
  . each find(): ~~O(1)
- Init result characters array: O(n)
- Sort 'indices' and 'chars': O(n*log(n))
  (worst case: all nodes are in the same connected component)
- Fill result characters array: O(n)
- Produce result string: O(n)

2. Space complexity: O(N + n) = O(n)
- 'uf': O(N)
- 'components': O(N)
- 'result' (characters array): O(n)
- Sorting: O(N) (timsort)
"""
