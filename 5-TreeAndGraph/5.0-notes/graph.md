# Definition

- A graph is a collection of nodes and connections between those nodes
- Other terms: nodes <=> vertices; connections <=> edges
- Special graph: binary tree
  - every node has at most 1 parent and 2 children

# Terminology

## Edge types

- directed: A -> B => can move from A to B, but not from B to A
- undirected: A - B => can move in both directions
- Special graph: binary tree
  - edges are directed (can only move from parent to children)

## Connected components

- A connected component of a graph is a group of nodes that are connected by edges
- Special graph: binary tree
  - there is only 1 connected component (all nodes are reachable from root)

## Degree and neighbors

- indegree: number of edges entering the node
- outdegree: number of edges leaving the node
- nodes that are connected by an edge are called neighbors
- Special graph: binary tree
  - all nodes except root have an indegree of 1 (edge coming from parent)
  - all nodes have an outdegree of 0, 1, 2
  - parent/child <=> neighbor

## Cyclic/acyclic

- cyclic: the graph has a cycle
- acyclic: the graph doesn't have a cycle
- Special graph: binary tree
  - cannot have a cycle

# In algorithmic problem

- With linked list and binary tree, we are given objects in memory that contain data and pointers (head, root).
- With graph problem, the graph doesn't literally exist in memory, only the "idea" of the graph exists.

## Input format

1. **array of edges**

- Input is a 2D array
- Each element is in the form [x, y], which indicate that there is an edge between x and y (directed or undirected)
- Let say we start DFS from node 0. To find the neighbors, we need to iterate over the entire input to find edges that include 0 (similar work when we move to a neighbor node) => `very slow`
  => Preprocess the input to find all neighbors of a node easily (use a hashmap)

```python
from collections import defaultdict

def build_graph(edges, directed):
    graph = defaultdict(list)
    for x, y in edges:
        graph[x].append(y)
        if not directed:
            graph[y].append(x)
    return graph
```

2. **adjacency list**

- nodes is numbered from 0 to n-1
- input `graph` is a 2D array
- `graph[i]` is the list of all outgoing edges from ith node
  => Easy to find all neighbors of a node

3. **adjacency matrix**

- nodes is numbered from 0 to n-1
- input `graph` is a 2D matrix of size n x n
- `graph[i][j] == 1` means there's an edge from node i to node j
- During traversal, for any given node, iterate over graph[node].
  If graph[node][i] == 1, i is a neighbor.
- We can preprocess the graph for faster lookup.

```python
from collections import defaultdict

def build_adjacency_list(adjacency_matrix):
    adjacency_list = defaultdict(list)
    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix[i])):
            if adjacency_matrix[i][j] == 1:
                adjacency_list[i].append(j)
    return adjacency_list
```

- Both approaches takes O(n^2) (traverse directly OR preprocess + traverse)

4. **matrix**

- input is a 2D matrix
- each square (row, col) is a node
- the neighbors are (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1) (if in bounds)

## Implementation details

- To prevent cycles / revisiting a node, we can use a set `seen`.
- For some language, it may be faster to use an array for `seen` if the range of states is known

# Tree graph

- In graph theory, a tree is a graph that satisfies 2 conditions:
  - Connected: every node is reachable from any other nodes
  - Acyclic: there are no cycles
- Note: ignore edge directions when deciding whether a graph is a tree.
- Property: for a graph with n nodes, if it is connected and has exactly n - 1 edges, it is guaranteed to be a tree

# When to use DFS/BFS

- There are some problems where using BFS is clearly better than using DFS
  - tree: when we concern with tree levels
  - graph: find the shortest path

# Implicit graph

- If a problem involves transitioning between states:
  - states can be nodes.
  - transition criteria can be edges.
- If a problem wants the shortest path or fewest operations etc.,
  it can be a candidate for BFS.
