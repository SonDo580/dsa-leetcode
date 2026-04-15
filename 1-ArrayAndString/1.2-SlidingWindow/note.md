- Used for problems that involve contiguous sub-arrays or substrings.
- Sliding window works when the quantity used to check the window's validity (sum, number of distinct characters, character frequency,...) exhibit monotonicity as the window moves:
  - When extending the right bound, this quantity changes in 1 direction.
  - When shrink the left bound, this quantity changes in the opposite direction.
- Based on this monotonic behavior, we can:
  - Easily check whether the current window is valid incrementally _(don't have to recalculating the constraint for the entire window)_
  - Avoid backtracking - each element is added and removed from the window at most once -> total time complexity is O(n)

## Examples

- the array only contains positive numbers -> extend from the right increases the sum, shrink from the left decrease the sum
- if the array also contains negative number -> extend from the right can increase or decrease the sum -> cannot use sliding window, since the property is not monotonic.
