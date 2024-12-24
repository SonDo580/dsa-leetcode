# Given the root node of a binary search tree 
# and two integers low and high,
# return the sum of values of all nodes with a value 
# in the inclusive range [low, high].

# ===== Trivial approach =====
# - use normal BFS or DFS, visit every node, 
#   add nodes whose values are between low and high

# ===== Leverage BST property =====
# - if current node's value is less than or equal to low, skip the left subtree
# - if current node's value is greater than or equal to high, skip the right subtree

class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right

def range_sum_bst_recursive(root: TreeNode, low: int, high: int) -> int:
    if not root:
        return 0
    
    sum = 0

    if low <= root.val <= high:
        sum += root.val

    if root.val > low:
        sum += range_sum_bst_recursive(root.left, low, high)

    if root.val < high:
        sum += range_sum_bst_recursive(root.right, low, high)

    return sum

def range_sum_bst_iterative(root: TreeNode, low: int, high: int) -> int:
    if not root:
        return 0
    
    sum = 0
    stack = [root]

    while len(stack) > 0:
        node = stack.pop()

        if low <= root.val <= high:
            sum += root.val

        if node.left and node.left.val > low:
            stack.append(node.left)

        if node.right and node.right.val < high:
            stack.append(node.right)

    return sum

# ===== Analyze =====
#
# Time complexity:
# - Is still O(n) - when all nodes are valid
# - But on average this algorithm will perform better than searching all nodes
# 
# Space complexity:
# - O(n) for the stack / recursion call