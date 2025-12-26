"""
https://leetcode.com/problems/the-earliest-moment-when-everyone-become-friends/

There are n people in a social group labeled from 0 to n - 1.
You are given an array `logs` where logs[i] = [timestamp_i, xi, yi]
indicates that xi and yi will be friends at the time timestamp_i.

Friendship is symmetric.
That means if a is friends with b, then b is friends with a.
Also, person a is acquainted with a person b if a is friends with b,
or a is a friend of someone acquainted with b.

Return the earliest time for which every person became acquainted with every other person.
If there is no such earliest time, return -1.
"""

"""
Analysis:
- Each person represents a node in a graph.
  A friendship represents a bidirectional edge.
- . person a becomes acquainted with person b
    <=> node a and node b are in the same connected component.
  . every person became acquainted with every other person
    <=> the number of connected components reduced to 1.
    
Solution: use UnionFind
- Initially, the number of connected components is count = n.
- `count` is decrement every time we perform `union`.
- Since we need to find the earliest time,
  sort the logs in increasing order of timestamp.
"""


class UnionFind:
    def __init__(self, n: int):
        self.ancestor = [i for i in range(n)]
        self.height = [0] * n
        self.count = n

    def find(self, x: int) -> int:
        if x == self.ancestor[x]:
            return x
        self.ancestor[x] = self.find(self.ancestor[x])
        return self.ancestor[x]

    def union(self, x: int, y: int):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return

        if self.height[root_x] > self.height[root_y]:
            self.ancestor[root_y] = root_x
        elif self.height[root_x] < self.height[root_y]:
            self.ancestor[root_x] = root_y
        else:
            self.ancestor[root_y] = root_x
            self.height[root_x] += 1
        self.count -= 1


def earliest_acquainted(logs: list[tuple[int, int, int]], n: int) -> int:
    logs.sort(key=lambda log: log[0])
    uf = UnionFind(n)
    for timestamp, person_1, person_2 in logs:
        uf.union(person_1, person_2)
        if uf.count == 1:
            return timestamp
    return timestamp if uf.count == 1 else -1


"""
Complexity:
- Let m = len(logs)
      n = number of people 

1. Time complexity: O(m * log(m))
- Sort 'logs': O(m * log(m))
- Loop through 'logs': O(m)
  . 'union' takes O(alpha(n)) ~ O(1)

2. Space complexity: O(m + n)
- Sort 'logs': O(m)
- UnionFind: O(n)
"""
