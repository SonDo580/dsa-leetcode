"""
https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/

There are n cities numbered from 0 to n - 1 and n - 1 roads
such that there is only one way to travel between two different cities.
Roads are represented by connections where connections[i] = [x, y]
represents a road from city x to city y. The edges are directed.
Swap the direction of some edges so that every city can reach city 0.
Return the minimum number of swaps needed.
"""

"""
Analysis:
- This is a directed graph given as an array of edges
  (cities are nodes, roads are edges).
- The graph is a tree graph (connected, has n nodes and n - 1 edges).
- For every city to be able to reach city 0,
  all roads must be directed towards 0
  -> 0 is the root of the tree graph.

Idea:
- Treat the graph as undirected, start traversing from city 0.
- Every time we see an edge pointing away, swap it and increment the count
  (an edge is pointing away if it is in 'connections' array).
"""


from collections import defaultdict


def min_reorder_recursive(connections: list[list[int]]) -> int:
    roads: set[tuple[int, int]] = set()
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in connections:
        graph[x].append(y)
        graph[y].append(x)
        roads.add((x, y))

    seen: set[int] = {0}  # visited nodes

    def dfs(node: int) -> int:
        """Return number of swaps need in node subtree."""
        swap_count = 0

        for neighbor in graph[node]:
            if neighbor not in seen:
                if (node, neighbor) in roads:
                    # edge is in 'connections'
                    # -> traversing away from city 0
                    # -> swap needed
                    swap_count += 1

                seen.add(neighbor)
                swap_count += dfs(neighbor)

        return swap_count

    return dfs(0)


def min_reorder_iterative(connections: list[list[int]]) -> int:
    roads: set[tuple[int, int]] = set()
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for x, y in connections:
        graph[x].append(y)
        graph[y].append(x)
        roads.add((x, y))

    swap_count = 0
    seen: set[int] = {0}  # visited nodes
    stack: list[int] = [0]

    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if neighbor not in seen:
                if (node, neighbor) in roads:
                    swap_count += 1
                seen.add(neighbor)
                stack.append(neighbor)

    return swap_count


"""
Complexity:
- Number of nodes: n
  Number of edges: E = n - 1
  Max depth: h 
  . worst case: h = O(n)

1. Time complexity: O(n + E) = O(n)
- visit each node once, each edge twice.

2. Space complexity: O(n)
- 'seen': O(n)
- 'roads': O(E) = O(n)
- 'graph': O(n + E) = O(n)
- stack:
  . recursive approach: O(h)
  . iterative approach: O(n)
"""
