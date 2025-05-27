# You are given the root node of a binary search tree (BST) and a value to insert into the tree.
# Return the root node of the BST after the insertion.
# It is guaranteed that the new value does not exist in the original BST.

# Notice that there may exist multiple valid ways for the insertion,
# as long as the tree remains a BST after insertion.
# You can return any of them.

# Example 1:
# Input: root = [4,2,7,1,3], val = 5
# Output: [4,2,7,1,3,5]

# Example 2:
# Input: root = [40,20,60,10,30,50,70], val = 25
# Output: [40,20,60,10,30,50,70,null,null,25]

# Example 3:
# Input: root = [4,2,7,1,3,null,null,null,null,null,null], val = 5
# Output: [4,2,7,1,3,5]

# Constraints:
# The number of nodes in the tree will be in the range [0, 10^4].
# -10^8 <= Node.val <= 10^8
# All the values Node.val are unique.
# -10^8 <= val <= 10^8
# It's guaranteed that val does not exist in the original BST.

from typing import Optional


class TreeNode:
    def __init__(
        self,
        val: int,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


def insert_into_bst_recur(root: TreeNode | None, val: int) -> TreeNode:
    if not root:
        return TreeNode(val)

    if val < root.val:
        root.left = insert_into_bst_recur(root.left, val)
    elif val > root.val:
        root.right = insert_into_bst_recur(root.right, val)
    return root


def insert_into_bst_iter(root: TreeNode | None, val: int) -> TreeNode:
    if not root:
        return TreeNode(val)

    current = root
    while current:
        if val < current.val:
            # insert into the left subtree
            if not current.left:
                current.left = TreeNode(val)
                break
            current = current.left
        elif val > current.val:
            # insert into the right subtree
            if not current.right:
                current.right = TreeNode(val)
                break
            current = current.right
        else:
            break  # val already exists

    return root


root = TreeNode(4)
root.left = TreeNode(2)
root.right = TreeNode(7)
root.left.left = TreeNode(1)
root.left.right = TreeNode(3)

x = insert_into_bst_iter(root, 5)
