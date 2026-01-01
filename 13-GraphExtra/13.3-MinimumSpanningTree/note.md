## Spanning Tree

- A spanning tree is a connected subgraph in an undirected graph where all vertices are connected with the minimum number of edges.

  - G(V, E) is an undirected graph.
  - T(V, F) is a subgraph of G (F is a subset of E).
  - If T is a tree then T is a spanning tree of G.

- Problem: Let G be an undirected graph. Check if G has a spanning tree.
  - G has a spanning tree <=> G is connected.
  - To check if a graph connected, perform DFS/BFS or use Union-Find. The final number of connected components must be 1.
  - Quick check: if E < N - 1, G is not connected (N - 1 is the number of edges in a tree).

## Minimum spanning tree

- Let G be a connected, undirected, weighted graph. For each spanning tree T, w(T) is the sum of all edges' weights. The tree with the smallest w(T) is called the `minimum spanning tree` of G.
- Problem: Let G be an undirected, weighted graph. Find 1 minimum spanning tree of G.

## Cut property
- A `cut` is is a partition of vertices in a graph into 2 disjoint subsets. A crossing edge is an edge that connects a vertex in 1 set with a vertex in the other set.
- Cut property: For any cut C of the graph, the minimum weight edge E of the cut-set belongs to all MSTs of the graph.

## Kruskal's algorithm

- Try to build T from the edges of G.
- First, sort the edges in ascending order of weights.
- At any given time, pick the edge with smallest weight to add to T (`greedy`). If adding an edge forms a cycle, skip it.
- Stop when the number of edges in T becomes N - 1 (N is the number of vertices) or when there're no edges left.
- To detect cycle, use Union-Find. If 2 ends of an edge are already in the same component tree, that edge forms a cycle.

## Prim's algorithm
- Maintain 2 sets of vertices - set 1 contains vertices already included in the MST, and set 2 contains vertices not yet included.
- Pick an arbitrary vertex as the starting vertex of the MST.
- At each step, consider all edges that connect the 2 sets (the cut-set) and pick the minimum weight edge (`greedy`).
- Add the chosen edge to the MST. Since we only consider edges that connect the 2 sets, we never get a cycle.
- Repeat until all vertices are included in the MST.