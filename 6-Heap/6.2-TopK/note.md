## "Find the k best elements" problem

1. Method 1: sort the input then return the top k element

- Time complexity: O(n\*log(n))

2. Method 2: use a heap with size k

- Time complexity: O(n\*log(k))
  k < n so this is an improvement

## Algorithm:

- Create a heap.
- Iterate over the input to push every element onto the heap.
- When the heap size exceed k, pop the "worst" element from it.
- At the end, the k "best" elements remain in the heap.

## Note on heapq implementation:
- If the items in the heap are tuples, it uses the first entries for comparison. 
- If the first entries are equal, it compares the second entries. 
- And so on.