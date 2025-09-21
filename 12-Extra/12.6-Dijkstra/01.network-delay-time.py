# You are given a network of n nodes, labeled from 1 to n.
# You are also given 'times', a list of travel times as directed edges.
# Each element in times is of the format [u, v, w],
# indicating that it takes w time for a signal to go from u to v.
# You are also given an integer k.  We will send a signal from node k.
# Return the minimum time it takes for every node to receive the signal.
# If it's impossible for all nodes to receive the signal, return -1.


# ===== Analysis =====
# - The graph is given as an array of edges.
#   Each edge has an associated weight (time).
# - time to traverse a path = path weight
# - The answer to the problem can be found by finding the shortest path
#   from k to every other node, then taking the maximum of those values.

# ===== Strategy =====
# - Create a hashmap to lookup node neighbors quickly.
#   + The nodes are labeled 1-indexed.
#   + When building the graph, subtract 1 to make them 0-indexed.
# - Run Dijkstra's algorithm on the graph, starting from k.
# - Return the maximum value in min_distances.
# - If the maximum value is infinity, it indicates that there are nodes
#   unreachable from k -> return -1.

from collections import defaultdict
import heapq


def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    graph = defaultdict(list)
    for x, y, weight in times:
        graph[x - 1].append((y - 1, weight))

    min_distances = [float("inf")] * n
    min_distances[k - 1] = 0
    heap = [(0, k - 1)]

    while heap:
        current_distance, node = heapq.heappop(heap)
        if current_distance > min_distances[node]:
            continue

        for neighbor, weight in graph[node]:
            neighbor_distance = current_distance + weight
            if neighbor_distance < min_distances[neighbor]:
                min_distances[neighbor] = neighbor_distance
                heapq.heappush(heap, (neighbor_distance, neighbor))

    answer = max(min_distances)
    return answer if answer < float("inf") else -1
