# Given the roots of two binary trees p and q,
# check if they are the same tree.
# Two binary trees are the same tree if they are structurally identical
# and the nodes have the same values.


class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def is_same_tree_recursive(p: TreeNode, q: TreeNode) -> bool:
    # Both are empty trees -> true
    if p == None and q == None:
        return True

    # 1 tree is empty but the other is not -> false
    if p == None or q == None:
        return False

    # Values of current nodes are different -> false
    if p.val != q.val:
        return False

    # The left and right subtrees of both trees must also be the same
    return is_same_tree_recursive(p.left, q.left) and is_same_tree_recursive(
        p.right, q.right
    )


def is_same_tree_iterative(p: TreeNode, q: TreeNode) -> bool:
    # Use (almost) the same code to check the cases
    # Only return True after we get through the tree without returning False

    stack = [(p, q)]

    while len(stack) > 0:
        p, q = stack.pop()

        # Both are empty trees -> pass current iteration
        if p == None and q == None:
            continue

        # 1 tree is empty but the other is not -> false
        if p == None or q == None:
            return False

        # Values of current nodes are different -> false
        if p.val != q.val:
            return False

        stack.append((p.left, q.left))
        stack.append((p.right, q.right))

    return True


# ===== Analysis =====
# Time complexity: O(n) where n is the number of nodes

# Space complexity: proportional to the height of the tree
# - worst case: O(n) when the tree is a straight line
# - best case: Ω(log n) when the tree is 'complete'
#
# complete tree: all nodes have 0 or 2 children and each level except the last is full
