# Identify a possible DP problem

- Solution can be built from solutions of sub-problems.
- Overlapping state / sub-problems (can avoid recomputation).
- Involve optimizing / counting.
- Local decision affect future choices.

# Compare with other methods

1. DP vs. Greedy

- Similarity: Aim to optimize something
- Differences:
  - DP: Local decision affects future
  - Greedy: Always use locally best choices

2. DP vs. Graph traversal vs. Backtracking

- Similarity: Involve an exploration process.
  - DP: explore sub-problems (traversal on state graph)
  - Backtracking: explore all possible choices (DFS on state graph)
  - Graph traversal: explore nodes/edges (traverse an explicit graph)
- Differences:
  - DP:
    - Handle overlapping sub-problems.
    - Avoid recomputation with memoization/tabulation.
  - Backtracking:
    - Explore all possible solutions.
    - Use pruning to cut infeasible paths.
  - Graph traversal:
    - Systematically visit nodes/edges without recomputation.
    - Used for reachability, connectivity, shortest paths,...
