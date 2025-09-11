# You are given an array 'equations' and a number array 'values' of the same length.
# equations[i] = [x, y] represents x / y = values[i].
# You are also given an array 'queries' where queries[i] = [a, b] which represents the quotient a / b.
# Return an array 'answer' where answer[i] is the answer to the ith query,
# or -1 if it cannot be determined.

# For example, let's say we have equations = [["a", "b"], ["b", "c"]] and values = [2, 3].
# This input represents a / b = 2 and b / c = 3.
# If we had a query ["a", "c"], the answer to that query would be 6,
# because we can deduce that a / c = 6.


# ===== Analyze =====
# - We can treat each variable as a node.
#   The edges are provided in 'equations'.
#   The weights of the edges are provided in 'values'.
# - The weight of the edge from x to y is the ratio x / y.
#   The reverse edge is the ratio y / x.
#   => When building the undirected graph:
#      when adding edge x -> y with weight x / y = val,
#      also add the edge y -> x with weight y / x = 1 / val
# - Let say we need to compute x / z.
#   There is edge x -> y with x / y weight
#   There is edge y -> z with y / z weight
#   => (x / y) * (y / z) = x / z, which is what we need
#   => We can traverse the graph from 'numerator' node with initial product 1.
#      Multiple the weight of an edge when we go through it.
#      Return the product if we can reach 'denominator' node.

# ===== Implementation notes =====
# - We can use DFS or BFS. Let's choose DFS
# - Build a hashmap to look up the neighbors of a node quickly.
#   Instead of using a list of nodes as in unweighted graph,
#   use a hashmap to store the edge's weight to reach a node.

from collections import defaultdict


def evaluate_division(
    equations: list[list[str]], values: list[float], queries: list[list[int]]
) -> list[float]:
    # Build the hashmap to lookup neighbor and edge's weight by node
    graph: defaultdict[int, dict[int, float]] = defaultdict(dict)
    for i in range(len(equations)):
        numerator, denominator = equations[i]
        ratio = values[i]
        graph[numerator][denominator] = ratio
        graph[denominator][numerator] = 1 / ratio

    def answer_query(numerator: int, denominator: int) -> float:
        if numerator not in graph or denominator not in graph:
            return -1

        seen: set[int] = {numerator}  # track visited node
        stack: list[tuple[int, float]] = [(numerator, 1)]  # (node, ratio)

        while stack:
            node, ratio = stack.pop()

            if node == denominator:
                return ratio

            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    weight = graph[node][neighbor]
                    stack.append((neighbor, ratio * weight))

        return -1

    answers: list[float] = []
    for numerator, denominator in queries:
        answers.append(answer_query(numerator, denominator))

    return answers


# ===== Complexity =====
# - Let: q be the length of queries
#        n be the number of nodes
#        e be the number of edges
#
# 1. Time complexity:
# - A graph traversal is performed for each query to find the answer,
#   which costs O(n + e)
# - We perform q traversals
# => Overall: O(q*(n + e))
#
# 2. Space complexity:
# - Space for 'seen': O(n)
# - Space for 'stack': O(n)
# - Space for 'answers': O(q)
# - Space for 'graph': O(n + e)
# => Overall: O(n + e + q)
