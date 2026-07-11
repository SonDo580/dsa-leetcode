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
- DFS (total): O(n + E)
- Sort 'indices' and 'chars': O(n*log(n))
  (worst case: all nodes are in the same connected component)
- Fill result characters array: O(n)
- Produce result string: O(n)

2. Space complexity: O(n + E)
- 'graph': O(n + E)
- 'visited': O(n)
- DFS stack: O(n)
- Sorting: O(n) (timsort)
- 'result': O(n)
"""
