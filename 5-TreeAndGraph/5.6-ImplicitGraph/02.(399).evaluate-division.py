"""
https://leetcode.com/problems/evaluate-division/

You are given an array 'equations' and a number array 'values' of the same length.
equations[i] = [x, y] represents x / y = values[i].
You are also given an array 'queries' where queries[i] = [a, b]
which represents the quotient a / b.
Return an array 'answer' where answer[i] is the answer to the ith query,
or -1 if it cannot be determined.

For example, let's say we have equations = [["a", "b"], ["b", "c"]] and values = [2, 3].
This input represents a / b = 2 and b / c = 3.
If we had a query ["a", "c"], the answer to that query would be 6,
because we can deduce that a / c = 6.
"""

"""
Idea:
- Treat each variable as a node.
  The edges are provided in 'equations'.
  The weights of the edges are provided in 'values'.
- The edge from x to y has weight x / y.
  The reverse edge has weight y / x.
  . weight x_y = val -> weight y_x = 1 / val
- Let say we need to compute x / z.
  There is edge x_y with weight x / y.
  There is edge y_z with weight y / z.
  -> (x / y) * (y / z) = x / z, which is what we need
  -> DFS/BFS from 'numerator' node with initial product 1.
     Multiply the weight of an edge when we go through it.
     Return the final product if we can reach 'denominator' node.

Implementation note:
- Build a hashmap to look up (neighbor + edge weight) of a node quickly:
  . Structure: graph[x][y] = weight
"""


from collections import defaultdict


def evaluate_division(
    equations: list[list[str]], values: list[float], queries: list[list[int]]
) -> list[float]:
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


"""
Complexity:
- Number of queries: q = len(queries)
  Number of nodes: N 
  Number of edges: E = len(equations)

1. Time complexity: O(E + q*(n + E)) = O(q*(n + E))
- Build 'graph': O(E)
- DFS for each query: O(N + E)
  -> O(q*(N + E)) for q queries

2. Space complexity: O(N + E)
- 'graph': O(N + E)
  . total 1st level keys: N
  . total 2nd level keys: 2*E
- 'seen': O(N)
- 'stack': O(N)
"""
