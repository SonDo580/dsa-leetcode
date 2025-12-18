# Tree

## Basic concepts

- Ancestor, children, descendants.
- Leaves: nodes with 0 children.
- Node depth: distance (edge count) from root to node.
  - root's depth = 0
- Node height: longest distance from node to a leaf in its subtree.
  - leaves' height = 0
  - root's height = tree's height

## Representation

```python
class TreeNode:
    def __init__(self, key):
        self.key = key
        self.children = []
```

# Binary tree

- Binary tree is a tree where each node has at most 2 children (left child and right child).

```python
class TreeNode:
    def __init__(self, key, left, right):
        self.key = key
        self.left = left
        self.right = right
```

## Special binary tree

- Full: every node other than the leaves has either 0 or 2 children
- Complete: all levels are completely filled except possibly the last level, which is filled from left to right.
- Degenerate (skewed): each node has only 1 child (becomes a linked list)
- Perfect (perfectly balanced): all internal nodes have exactly 2 children and all leaf nodes are at the same level **(full + complete)**.
- Balanced: the height difference between the left and right subtrees of any node is at most 1.
  - often an AVL tree or Red-Black tree.
  - automatically perform rotations to keep the property.

## Traversal

- in-order (DFS): left -> node -> right
- pre-order (DFS): node -> left -> right
- post-order (DFS): left -> right -> node
- level-order (BFS)

# Binary search tree

## Property

- BST is a type of binary tree.
- For each node:
  - all values in its left subtree are less than the node value.
  - all values in its right subtree are greater than the node value.
- This implies that all values in a BST are unique.
- An in-order traversal on a BST handle the nodes in sorted order.

## Complexity

- Both Search, Insert, Delete have average time complexity O(log(n)).
- In the worst case, the time complexity is O(n) (all nodes only have 1 child -> the tree becomes a linked list).

## Why not just use sorted array

- Although performing binary search on sorted array takes O(log(n)),
  insert and delete take O(n) due to elements shifting.
