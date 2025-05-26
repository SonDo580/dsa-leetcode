# Property

- BST is a type of binary tree.
- For each node:
  - all values in its left subtree are less than the node value.
  - all values in its right subtree are greater than the node value.
- This implies that all values in a BST are unique.
- An in-order DFS traversal on a BST handle the nodes in sorted order.

# Complexity

- Both Search, Insert, Delete have average time complexity O(log(n)).
- In the worst case, the time complexity is O(n) (for example, all the nodes only have right child -> the tree becomes a linked list).
