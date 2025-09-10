# You are given a directed graph with n nodes labeled from 0 to n - 1.
# Edges are red or blue in this graph.
#
# You are given redEdges and blueEdges,
# where redEdges[i] and blueEdges[i] both have the format [x, y]
# indicating an edge from x to y in the respective color.
#
# Return an array ans of length n,
# where answer[i] is the length of the shortest path from 0 to i
# where edge colors alternate, or -1 if no path exists.


# ===== Analyze =====
# - We start at node 0 and need to find the shortest path to all other nodes.
# - Normally, a BFS with a steps variable can accomplish this.
# - But the edges must also be alternating in color
#   -> Store color to use for the next edge.
# - Treat (node, color) as a state

# ===== Implementation notes =====
# - Start the BFS from both (0, RED) and (0, BLUE).
# - Switch edge color when move to a new node. One way to switch color is:
#   + assign RED = 0 and BLUE = 1 (or vice versa, doesn't matter)
#   + switch formula: color = 1 - color
# - The 'seen' set should track visited states (node, color).
#   (Paths that reach node through different colors are different)
# - Build a hashmap to lookup neighbors of a node.
#   Add a layer to group neighbors accessed through edges of a color.
#   Structure:
#   + graph[node][color] OR graph[color][node] are both OK
#   + Let's use graph[color][node] to reduce number of keys

from collections import defaultdict, deque


def shortest_path_with_alternate_color(
    n: int, red_edges: list[list[int]], blue_edges: list[list[int]]
) -> list[int]:
    RED = 0
    BLUE = 1

    # Build hash map to look up neighbors
    # Group neighbors accessed through edges of a color
    graph: defaultdict[int, defaultdict[int, list]] = defaultdict(
        lambda: defaultdict(list)
    )
    for x, y in red_edges:
        graph[RED][x].append(y)
    for x, y in blue_edges:
        graph[BLUE][x].append(y)

    # Initialize shortest path to reach each node
    ans = [float("inf")] * n

    # Item: (node, next edge color to use, number of steps so far)
    queue: deque[tuple[int, int, int]] = deque([(0, RED, 0), (0, BLUE, 0)])

    # Track visited states: (node, next edge color to use)
    seen: set[tuple[int, int]] = {(0, RED), (0, BLUE)}

    while queue:
        node, color, steps = queue.popleft()
        ans[node] = min(ans[node], steps)

        for neighbor in graph[color][node]:
            if (neighbor, 1 - color) not in seen:
                seen.add((neighbor, 1 - color))
                queue.append((neighbor, 1 - color, steps + 1))

    # The nodes with infinity distance are not reached -> use -1
    return [x if x != float("inf") else -1 for x in ans]
