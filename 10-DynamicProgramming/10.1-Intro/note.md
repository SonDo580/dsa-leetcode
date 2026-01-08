# Identify a possible DP problem

- Solution can be built from solutions of sub-problems.
- Overlapping state / sub-problems (can avoid recomputation).
- Involve optimizing / counting.
- Local decision affect future choices.

# Framework

1. A function or data structure that computes/contains the answer to the problem for any given state.
2. A recurrence function to transition between states.
3. Base case.

# Approaches

- Top-down (recursion + memoization)
- Bottom-up (tabulation)

# Compare top-down and bottom-up

## Order

- Top-down:
  - don't have to care about sub-problem order (handled naturally by recursion).
- Bottom-up:
  - must solve sub-problems in correct order.

## State mapping

- Top-down:
  - flexible, can use hashmap for negative or large integers, non-integers, sparse states.
- Bottom-up:
  - restricted to array indices, need special handling for negative or very large indices.

## Computation and Efficiency

- Top-down:
  - only solve sub-problems reachable from the root -> faster in problems with sparse state space.
  - function call overhead (from recursion) and constant-time overhead of hashmap lookup -> slower for problems with dense state space.
- Bottom-up:
  - must solve all sub-problems, even the ones that are not needed for final result.

## Memory

- Top-down:
  - need memory for both memoization table and recursion.
  - recursion can cause stack overflow.
- Bottom-up:
  - no stack overflow risk.
  - space can be optimized if the recurrence relation is static.

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
