# Given the root of a binary tree and two nodes p and q that are in the tree,
# return the lowest common ancestor (LCA) of the two nodes.
# The LCA is the lowest node in the tree that has both p and q as descendants
# (note: a node is a descendant of itself).


class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


# Possibilities:
# - empty tree -> no LCA exists
# - the root node is p or q -> the answer cannot be below the root node
# - 1 of p or q is in the left subtree, the other is in the right subtree
#   -> the root is the LCA because it connects 2 subtrees
# - both p and q are in 1 of the subtree
#   -> look inside that subtree and find a lower node


def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode | None:
    # Base case: empty tree -> no LCA exists
    if not root:
        return None

    # If the root node is p or q -> it must be the LCA
    if root == p or root == q:
        return root

    # Look for the LCA in the left and right subtrees
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    # If 1 of p or q is in the left subtree, the other is in the right subtree
    # -> the root node is the LCA
    if left and right:
        return root

    # if both p and q are in 1 subtree
    # -> return the LCA found from the recursive call
    if left:
        return left
    else:
        return right


# ===== Analysis =====
# Time complexity: O(n) where n is the number of nodes
# (each node is visited at most once and constant work is done at each node)

# Space complexity: proportional to the height of the tree
# - worst case: O(n) when the tree is a straight line
# - best case: Ω(log n) when the tree is 'complete'
#
# complete tree: all nodes have 0 or 2 children and each level except the last is full
