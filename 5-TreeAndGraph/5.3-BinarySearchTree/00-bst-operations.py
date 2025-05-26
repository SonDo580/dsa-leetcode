class TreeNode:
    def __init__(
        self, val: int, left: "TreeNode" | None = None, right: "TreeNode" | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def search(root: TreeNode | None, val: int) -> TreeNode | None:
    """Search for a node with value."""
    if not root:
        return None

    if val < root.val:
        return search(root.left)
    if val > root.val:
        return search(root.right)
    return root


def insert(root: TreeNode | None, val: int) -> TreeNode:
    """Insert a node into the tree. Return the root."""
    if not root:
        return TreeNode(val)

    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root


def delete(root: TreeNode | None, val: int):
    """
    Delete a node from a tree. Return the root (with possibly new value).
    There are 3 cases:
    - node has no children: just remove it.
    - node has one child: replace the node with its only child.
    - node has 2 children:
        + find min_node in the right subtree
        + replace node's value with that min_node's value
        + (recursively) delete the min_node in the right subtree
        + note: min_node is the left-most node in the right subtree (no left child).
                so its deletion will hit case 1 or case 2.
    """
    if not root:
        return root

    if val < root.val:
        root.left = delete(root.left, val)
    elif val > root.val:
        root.right = delete(root.right, val)
    else:
        # Node found

        # Node has no children or 1 child
        if not root.left:
            return root.right
        if not root.right:
            return root.left

        # Node has 2 children
        right_min_node = _find_min(root.right)
        root.val = right_min_node.val
        root.right = delete(root.right, right_min_node.val)

    return root


def _find_min(node: TreeNode) -> TreeNode:
    """Find the minimum node in a BST (the left-most one)"""
    current = node
    while current.left:
        current = current.left
    return current
