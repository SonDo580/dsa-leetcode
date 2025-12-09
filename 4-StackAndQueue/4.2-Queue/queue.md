## Types

- Normal queue allows:

  - enqueue at the back.
  - dequeue at the front.

- Double-ended queue allows:
  - insert to both ends.
  - remove from both ends.

## Implementation

- Using a dynamic array works but is inefficient. Removing the first element would take O(n) since all other elements have to move.

- Some options to implement an efficient queue:

  - Use a singly linked list that maintains pointers to the head and tail (sentinel nodes).
  - Use 2 stacks (2 dynamic arrays, 1 for enqueuing and 1 for dequeuing).

- Some options to implement an efficient double-ended queue:

  - Use a doubly linked list that maintains pointers to the head and tail (sentinel nodes).
  - Use a blocked linked list (linked list of fixed-size arrays). 

- See examples in `queue-self-implemented` and `deque-self-implemented`.
