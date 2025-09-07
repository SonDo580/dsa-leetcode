# There are n cities numbered from 0 to n - 1 and n - 1 roads
# such that there is only one way to travel between two different cities.
# Roads are represented by connections where connections[i] = [x, y]
# represents a road from city x to city y. The edges are directed.
# Swap the direction of some edges so that every city can reach city 0.
# Return the minimum number of swaps needed.

# ===== Analyze =====
# - This is a directed graph given as an array of edges.
# - The graph is a tree (see 5.0-notes/graph.md):
#   + there are n nodes and n - 1 edges
#   + there is only 1 path between 2 nodes
# - If every city can reach city 0, all roads must be directed towards 0
#   (0 is the root of the tree)

# ===== Strategy =====
# - Treat the graph as undirected, start traversing from city 0
# - Every time we see an edge pointing away, swap it and increment the count
#   (an edge is pointing away if it is present in 'connections' array)

from collections import defaultdict


def min_reorder_recursive(connections: list[list[int]]) -> int:
    roads = set()  # to fast-check if an edge is in 'connections'
    graph = defaultdict(list)  # represent as adjacency list

    for x, y in connections:
        graph[x].append(y)
        graph[y].append(x)
        roads.add((x, y))

    seen = {0}  # track visited nodes

    def dfs(node):
        swap_count = 0  # number of swaps needed

        # visit the neighbors
        for neighbor in graph[node]:
            if neighbor not in seen:
                # We are traversing away from city 0.
                # So if the edge is in 'connections', we need to swap it.
                if (node, neighbor) in roads:
                    swap_count += 1

                # mark the neighbor as visited
                seen.add(neighbor)

                swap_count += dfs(neighbor)

        return swap_count

    return dfs(0)  # start from 0


def min_reorder_iterative(connections: list[list[int]]) -> int:
    roads = set()
    graph = defaultdict(list)
    for x, y in connections:
        graph[x].append(y)
        graph[y].append(x)
        roads.add((x, y))

    swap_count = 0
    seen = {0}
    stack = [0]

    while len(stack) > 0:
        node = stack.pop()

        for neighbor in graph[node]:
            if neighbor not in seen:
                if (node, neighbor) in roads:
                    swap_count += 1
                    
                seen.add(neighbor)
                stack.append(neighbor)

    return swap_count


# ===== Complexity =====
#
# Time complexity:
# - we visit each node once and do constant work -> O(n)
# - we visit each edge twice -> O(2(n-1)) = O(n)
# => Overall: O(n)
#
# Space complexity:
# - seen: O(n)
# - roads: O(n-1) = O(n)
# - graph: O(n)
# - recursion stack / stack: O(n)
# => Overall: O(n)
